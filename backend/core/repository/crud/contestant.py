from typing import Sequence

from sqlalchemy import select

from backend.core.models import (
    Contestant,
    User,
)
from backend.core.repository.crud.base import BaseCRUDRepository
from backend.core.utilities.loggers.log_decorator import log_calls
from cryptography.fernet import Fernet
from backend.configuration.settings import settings

fernet = Fernet(settings.FERNET_KEY)


class ContestantCRUDRepository(BaseCRUDRepository):

    @log_calls
    async def get_contestant_by_id(
            self,
            contestant_id: int,
    ) -> Contestant | None:
        res = await self.async_session.execute(
            select(Contestant)
            .where(Contestant.id == contestant_id)
        )
        res = res.scalar_one_or_none()
        return res

    @log_calls
    async def get_contestant_by_user_id(
            self,
            user_id: int
    ) -> Contestant | None:
        res = await self.async_session.execute(
            select(Contestant)
            .join(User, User.id == Contestant.user_id)
            .where(User.id == user_id)
        )
        res = res.scalar_one_or_none()
        return res

    @log_calls
    async def create_contestant(
            self,
            user_id: int,
            password: str,
            name: str,
            points: int,
    ) -> Contestant:
        contestant: Contestant = (
            Contestant(
                user_id=user_id,
                name=name,
                points=points,
                password_encrypted=fernet.encrypt(password.encode()).decode(),  # base64
            )
        )
        self.async_session.add(instance=contestant)
        await self.async_session.flush()
        # await self.async_session.commit()

        return contestant

    @log_calls
    async def get_contestants_in_contest(
            self,
            contest_id: int,
    ) -> Sequence[Contestant]:
        rows = await self.async_session.execute(
            select(Contestant)
            .join(User, User.id == Contestant.user_id)
            .where(User.domain_number == contest_id)
        )
        result = rows.scalars().all()
        return result


"""
Пример вызова

contestant_repo = get_repository(
    repo_type=ContestantCRUDRepository
)
"""
