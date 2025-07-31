import uuid

from sqlalchemy import select

from backend.core.models.user import User
from backend.core.repository.crud.base import BaseCRUDRepository
from backend.core.services.security import (
    hash_password,
    verify_password,
    create_access_token,
)
from backend.core.utilities.exceptions.auth import TokenException
from backend.core.utilities.exceptions.database import EntityAlreadyExists
from backend.core.utilities.loggers.log_decorator import log_calls


class UserCRUDRepository(BaseCRUDRepository):
    @log_calls
    async def create_site_user(
            self,
            username: str,
            password: str,
    ) -> User:
        user_exists: User = await self.async_session.scalar(
            select(User)
            .where(
                User.username == username,
                User.domain_number == 0
            )
        )
        if user_exists:
            raise EntityAlreadyExists("Account with id `{id}` already exist!")

        user = User(
            domain_number=0,
            username=username,
            hashed_password=hash_password(password),
            uuid=str(uuid.uuid4())
        )
        self.async_session.add(instance=user)
        # await self.async_session.flush()
        await self.async_session.commit()  # Оставить!
        await self.async_session.refresh(user)  # Оставить!

        return user

    @log_calls
    async def create_contest_user(
            self,
            domain_number: int,
            username: str,
            password: str,
    ) -> User:
        user_exists: User = await self.async_session.scalar(
            select(User)
            .where(
                User.username == username,
                User.domain_number == domain_number
            )
        )
        if user_exists:
            raise EntityAlreadyExists("Account with id `{id}` already exist!")

        user = User(
            domain_number=domain_number,
            username=username,
            hashed_password=hash_password(password),
            uuid=str(uuid.uuid4())
        )
        self.async_session.add(instance=user)
        await self.async_session.flush()
        # await self.async_session.commit()
        # await self.async_session.refresh(user)

        return user

    @log_calls
    async def authenticate_user(
            self,
            domain_number: int,
            username: str,
            password: str,
    ):
        user: User = await self.async_session.scalar(
            select(User)
            .where(
                User.username == username,
                User.domain_number == domain_number
            )
        )
        if not user or not verify_password(password, user.hashed_password):
            raise TokenException("Invalid credentials")

        # todo: что это делает тут? переместить позже
        return create_access_token({"sub": user.uuid})

    @log_calls
    async def get_user_by_username_and_domain(
            self,
            username: str,
            domain_number: int,
    ) -> User | None:
        res = await self.async_session.execute(
            select(User)
            .where(
                User.username == username,
                User.domain_number == domain_number
            )
        )
        user = res.scalar_one_or_none()
        return user

    @log_calls
    async def get_user_by_uuid(
            self,
            user_uuid: str,
    ) -> User | None:
        res = await self.async_session.execute(
            select(User)
            .where(User.uuid == user_uuid)
        )
        user = res.scalar_one_or_none()
        return user

    @log_calls
    async def get_user_by_id(
            self,
            user_id: int,
    ) -> User | None:
        """
        Возвращает объект User с указанным id
        :param user_id: id объекта User
        :return: объект User c указанным user_id или None
        """
        res = await self.async_session.execute(
            select(User)
            .where(User.id == user_id)
        )
        return res.scalars().one_or_none()


"""
Пример вызова

user_repo = get_repository(
    repo_type=UserCRUDRepository
)
"""
