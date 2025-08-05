from typing import Sequence

from sqlalchemy.sql.functions import func

from backend.core.models.contestant_log import (
    ContestantLogLevelType,
    ContestantLog,
)
from sqlalchemy import select
from backend.core.repository.crud.base import BaseCRUDRepository
from backend.core.utilities.loggers.log_decorator import log_calls


class ContestantLogCRUDRepository(BaseCRUDRepository):

    @log_calls
    async def create_log(
            self,
            contestant_id: int,
            log_level: ContestantLogLevelType,
            content: str,
    ) -> ContestantLog:
        contestant_log: ContestantLog = (
            ContestantLog(
                contestant_id=contestant_id,
                level_type=log_level,
                content=content,
            )
        )
        self.async_session.add(instance=contestant_log)
        await self.async_session.flush()
        return contestant_log

    @log_calls
    async def count_logs_by_contestant_id(self, contestant_id: int) -> int:
        stmt = select(func.count()).select_from(ContestantLog).where(ContestantLog.contestant_id == contestant_id)
        result = await self.async_session.execute(stmt)
        return result.scalar_one()

    @log_calls
    async def get_contestant_logs_in_contest(
            self,
            contestant_id: int,
            offset: int = 0,
            limit: int = 100,
    ) -> Sequence[ContestantLog]:
        stmt = (
            select(ContestantLog)
            .where(ContestantLog.contestant_id == contestant_id)
            .order_by(ContestantLog.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await self.async_session.execute(stmt)
        return result.scalars().all()


"""
Пример вызова

contestant_log_repo = get_repository(
    repo_type=ContestantLogCRUDRepository
)
"""
