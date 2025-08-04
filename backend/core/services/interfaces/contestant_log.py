"""
Интерфейс сервиса для работы с логами участников контеста.

Это не системные логи. Это "уведомления" или "сообщения", видимые участником на странице контеста.
"""

from typing import Protocol

from backend.core.models.contestant_log import ContestantLogLevelType
from backend.core.schemas.contestant_log import ContestantLogId


class IContestantLogService(Protocol):
    """
    Протокол (интерфейс) сервиса управления участниками контестов.
    Описывает методы для работы с участниками, которые должны быть реализованы в сервисе.
    """

    async def create_contestant_log(
            self,
            contestant_id: int,
            log_level: ContestantLogLevelType = ContestantLogLevelType.DEBUG,
            content: str = '',
    ) -> ContestantLogId:
        ...
