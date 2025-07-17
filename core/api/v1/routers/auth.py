from typing import Annotated

import fastapi
from fastapi import Depends, HTTPException, Body
from fastapi import Security
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, Request, Response

from core.dependencies.authorization import oauth2_scheme, get_user
from core.dependencies.repository import get_repository
from core.forms.authorization import CustomLoginForm
from core.models.user import User
from core.repository.crud.user import UserCRUDRepository
from core.schemas.user import SiteUserCreate, UserOut, Token, RefreshToken
from core.services.domain import auth as auth_service
from core.services.domain.auth import verify_refresh_token
from core.services.security import REFRESH_TOKEN_EXPIRE_MINUTES, create_refresh_token, create_access_token
from core.utilities.exceptions.auth import UnauthorizedException, TokenException
from core.utilities.exceptions.database import EntityAlreadyExists
from core.utilities.exceptions.handlers.http400 import async_http_exception_mapper

router = fastapi.APIRouter(prefix="/auth", tags=["authentication"])

#
# @router.post(
#     path="/block-my-token",
#     status_code=204,
# )
# async def push_token_to_blacklist(
#         params: RefreshToken = Body(...),
#         user: User = Depends(get_user),
#         user_repo: UserCRUDRepository = Depends(get_repository(UserCRUDRepository)),
# ):



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
async def login_for_access_token(
        response: Response,
        # form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        form_data: Annotated[CustomLoginForm, Depends()],
        user_repo: UserCRUDRepository = Depends(get_repository(UserCRUDRepository)),
) -> dict[str, str]:
    """"""
    try:
        access_token: str = (
            await auth_service.authenticate_user(
                domain_number=form_data.domain_number,
                username=form_data.username,
                password=form_data.password,
                user_repo=user_repo,
            )
        )
        refresh_token: str = (
            create_refresh_token(
                data={"sub": form_data.username},
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

        return {"access_token": access_token, "token_type": "bearer"}

    except TokenException as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    path="/refresh",
)
async def refresh_access_token(
        request: Request,
        user_repo: UserCRUDRepository = Depends(get_repository(UserCRUDRepository)),
) -> dict[str, str]:
    """"""
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