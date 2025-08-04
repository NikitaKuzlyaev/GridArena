from typing import Protocol

from backend.core.models.contestant_log import ContestantLogLevelType
from backend.core.schemas.contestant_log import ContestantLogId
from backend.core.utilities.loggers.log_decorator import log_calls


class IContestantLogService(Protocol):
    """
    Протокол (интерфейс) сервиса управления участниками контестов.
    Описывает методы для работы с участниками, которые должны быть реализованы в сервисе.
    """

    @log_calls
    async def create_contestant_log(
            self,
            contestant_id: int,
            log_level: ContestantLogLevelType = ContestantLogLevelType.DEBUG,
            content: str = '',
    ) -> ContestantLogId:
        ...
