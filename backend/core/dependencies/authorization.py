from typing import Tuple

from fastapi import (
    Depends,
    HTTPException,
)
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from backend.core.dependencies.repository import get_repository
from backend.core.models.user import User
from backend.core.repository.crud.user import UserCRUDRepository
from backend.core.services.domain import auth as auth_service
from backend.core.utilities.exceptions.database import EntityDoesNotExist
from backend.core.utilities.loggers.log_decorator import log_calls
from backend.handlers.token_blacklist.impl.main.provider import get_token_blacklist_handler
from backend.handlers.token_blacklist.interface import ITokenBlacklistHandler

oauth2_schema = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

from backend.core.services.security import decode_token


@log_calls
async def get_user(
        token: str = Depends(oauth2_schema),
        token_blacklist_handler: ITokenBlacklistHandler = Depends(get_token_blacklist_handler),
        user_repo: UserCRUDRepository = Depends(get_repository(UserCRUDRepository)),
) -> User:
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    is_token_in_blacklist: bool = (
        await token_blacklist_handler.check_token_in_blacklist(
            token=token,
        )
    )
    if is_token_in_blacklist:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = decode_token(token=token)
        user_uuid: str = payload.get("sub")

        if user_uuid is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")

        user: User = (
            await auth_service.get_user_by_uuid(
                user_uuid=user_uuid,
                user_repo=user_repo,
            )
        )

        return user

    except EntityDoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Could not validate credentials")


#
# ДЛЯ ДЕБАГА!!!
#
@log_calls
async def get_user_with_access_token(
        token: str = Depends(oauth2_schema),
        user_repo: UserCRUDRepository = Depends(get_repository(UserCRUDRepository)),
) -> Tuple[User, str]:
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = decode_token(token=token)
        user_uuid: str = payload.get("sub")

        if user_uuid is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")

        user: User = (
            await auth_service.get_user_by_uuid(
                user_uuid=user_uuid,
                user_repo=user_repo,
            )
        )

        return user, token

    except EntityDoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
