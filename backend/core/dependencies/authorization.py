from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from backend.core.dependencies.repository import get_repository
from backend.core.models.user import User
from backend.core.repository.crud.user import UserCRUDRepository
from backend.core.services.domain import auth as auth_service
from backend.core.utilities.exceptions.database import EntityDoesNotExist

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

from backend.core.services.security import decode_token


async def get_user(
        token: str = Depends(oauth2_scheme),
        user_repo: UserCRUDRepository = Depends(get_repository(UserCRUDRepository)),
) -> User:
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

        return user

    except EntityDoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
