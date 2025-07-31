from backend.core.models.user import User
from backend.core.repository.crud.user import UserCRUDRepository
from backend.core.schemas.user import SiteUserCreate
from backend.core.services.security import decode_token
from backend.core.utilities.exceptions.auth import TokenException
from backend.core.utilities.exceptions.database import (
    EntityDoesNotExist,
    EntityAlreadyExists,
)
from backend.core.utilities.loggers.log_decorator import log_calls


# todo: жесть тут грязно и как же этот "сервис" отличается от остальных

@log_calls
async def register_site_user(
        data: SiteUserCreate,
        user_repo: UserCRUDRepository,
) -> User:
    try:
        user: User = (
            await user_repo.create_site_user(
                username=data.username,
                password=data.password,
            )
        )
        return user
    except EntityAlreadyExists:
        raise EntityAlreadyExists("Пользователь с таким username уже существует в указанном домене")


# @log_calls
# async def register_contest_user(
#         data: SiteUserCreate,
#         user_repo: UserCRUDRepository,
# ) -> User:
#     user: User = (
#         await user_repo.create_site_user(
#             username=data.username,
#             password=data.password,
#         )
#     )
#     return user


@log_calls
async def verify_refresh_token(
        token: str,
        user_repo: UserCRUDRepository,
) -> User | None:
    try:
        payload = decode_token(token=token)
        user_uuid: str = payload.get("sub")
        token_type: str = payload.get("token_type")

        if user_uuid is None or token_type is None or token_type != 'refresh':
            raise TokenException("Invalid authentication credentials")

        user: User = (
            await user_repo.get_user_by_uuid(
                user_uuid=user_uuid,
            )
        )

        return user

    except TokenException as e:
        raise e
    except EntityDoesNotExist as e:
        raise e
    except Exception as e:
        raise e


@log_calls
async def authenticate_user(
        domain_number: int,
        username: str,
        password: str,
        user_repo: UserCRUDRepository,
) -> str:
    token: str = (
        await user_repo.authenticate_user(
            domain_number=domain_number,
            username=username,
            password=password,
        )
    )
    return token


@log_calls
async def get_user_by_uuid(
        user_uuid: str,
        user_repo: UserCRUDRepository,
) -> User:
    user: User = (
        await user_repo.get_user_by_uuid(
            user_uuid=user_uuid,
        )
    )
    if not user:
        raise EntityDoesNotExist

    return user
