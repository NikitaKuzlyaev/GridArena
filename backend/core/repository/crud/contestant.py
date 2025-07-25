from typing import Sequence

from sqlalchemy import select

from backend.core.dependencies.repository import get_repository
from backend.core.models import Contestant, User
from backend.core.repository.crud.base import BaseCRUDRepository
from backend.core.utilities.loggers.log_decorator import log_calls


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
            name: str,
            points: int,
    ) -> Contestant:
        contestant: Contestant = (
            Contestant(
                user_id=user_id,
                name=name,
                points=points,
            )
        )
        self.async_session.add(contestant)
        await self.async_session.commit()

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


contestant_repo = get_repository(
    repo_type=ContestantCRUDRepository
)
