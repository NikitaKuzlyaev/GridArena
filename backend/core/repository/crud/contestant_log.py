from backend.core.models.contestant_log import (
    ContestantLogLevelType,
    ContestantLog,
)
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


"""
Пример вызова

contestant_log_repo = get_repository(
    repo_type=ContestantLogCRUDRepository
)
"""
