from typing import Annotated

import fastapi
from fastapi import Depends, Request, Response
from fastapi import HTTPException
from starlette.responses import JSONResponse

from backend.core.dependencies.authorization import get_user_with_access_token
from backend.core.dependencies.repository import get_repository
from backend.core.forms.authorization import CustomLoginForm
from backend.core.models.user import User
from backend.core.repository.crud.user import UserCRUDRepository
from backend.core.schemas.user import SiteUserCreate, UserOut, Token, UserType
from backend.core.services.domain import auth as auth_service
from backend.core.services.domain.auth import verify_refresh_token
from backend.core.services.security import REFRESH_TOKEN_EXPIRE_MINUTES, create_refresh_token, create_access_token
from backend.core.utilities.exceptions.auth import TokenException
from backend.core.utilities.exceptions.database import EntityAlreadyExists
from backend.core.utilities.exceptions.handlers.http400 import async_http_exception_mapper
from backend.handlers.token_blacklist.impl.main.provider import get_token_blacklist_handler
from backend.handlers.token_blacklist.interface import ITokenBlacklistHandler

router = fastapi.APIRouter(prefix="/auth", tags=["authentication"])


@router.post(
    path="/register",
    response_model=UserOut,
)
@async_http_exception_mapper(
    mapping={
        EntityAlreadyExists: (409, None),
    }
)
async def register(
        data: SiteUserCreate,
        user_repo: UserCRUDRepository = Depends(get_repository(UserCRUDRepository)),
):
    user: User = (
        await auth_service.register_site_user(
            data=data,
            user_repo=user_repo,
        )
    )
    return user


@router.post(
    path="/login",
    response_model=Token,
    status_code=200,
)
@async_http_exception_mapper(
    mapping={
        TokenException: (401, None),
    }
)
async def login_for_access_token(
        response: Response,
        form_data: Annotated[CustomLoginForm, Depends()],
        user_repo: UserCRUDRepository = Depends(get_repository(UserCRUDRepository)),
) -> Token:
    access_token: str = (
        await auth_service.authenticate_user(
            domain_number=form_data.domain_number,
            username=form_data.username,
            password=form_data.password,
            user_repo=user_repo,
        )
    )
    user: User = (
        await user_repo.get_user_by_username_and_domain(
            username=form_data.username,
            domain_number=form_data.domain_number,
        )
    )
    refresh_token: str = (
        create_refresh_token(
            data={"sub": user.uuid},
        )
    )
    max_age = REFRESH_TOKEN_EXPIRE_MINUTES

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        #
        # secure=True,
        # ТОЛЬКО В ДЕБАГЕ!!!
        secure=True,
        #
        # samesite="lax",
        # Только в ДЕБАГЕ!!!
        samesite="none",
        #
        max_age=max_age * 60,
        path='/',
    )

    res = Token(
        access_token=access_token,
        token_type="bearer",
        user_type=UserType.SITE if user.domain_number == 0 else UserType.CONTEST,
    )

    return res


@router.post(
    path="/refresh",
)
async def refresh_access_token(
        request: Request,
        user_repo: UserCRUDRepository = Depends(get_repository(UserCRUDRepository)),
) -> dict[str, str]:
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing.")

    user: User | None = (
        await verify_refresh_token(
            token=refresh_token,
            user_repo=user_repo,
        )
    )
    if not user:
        raise HTTPException(status_code=401, detail="User not found.")

    new_access_token = create_access_token(data={"sub": user.username})
    return {"access_token": new_access_token, "token_type": "bearer"}


@router.post(
    path="/block-my-token",
)
async def move_user_tokens_to_blacklist(
        request: Request,
        user_with_access_token: User = Depends(get_user_with_access_token),
        user_repo: UserCRUDRepository = Depends(get_repository(UserCRUDRepository)),
        token_blacklist_handler: ITokenBlacklistHandler = Depends(get_token_blacklist_handler),
) -> JSONResponse:
    user, access_token = user_with_access_token

    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing.")

    user_from_refresh_token: User | None = (
        await verify_refresh_token(
            token=refresh_token,
            user_repo=user_repo,
        )
    )
    if not user_from_refresh_token:
        raise HTTPException(status_code=401, detail="User not found.")
    if user.username != user_from_refresh_token.username:
        raise HTTPException(status_code=403, detail="Permission denied.")

    try:
        coro_1 = token_blacklist_handler.move_token_to_blacklist(
            token=refresh_token,
            expires_in_seconds=REFRESH_TOKEN_EXPIRE_MINUTES * 60 * 2,
        )
        coro_2 = token_blacklist_handler.move_token_to_blacklist(
            token=access_token,
            expires_in_seconds=REFRESH_TOKEN_EXPIRE_MINUTES * 60 * 2,
        )
        await coro_1
        await coro_2
    except:
        raise HTTPException(status_code=503, detail="Service for check user token temporarily unavailable.")

    return JSONResponse({'success': True})
