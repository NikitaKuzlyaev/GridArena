"""
Интерфейс сервиса для работы с отправками решений.

Определяет контракт для реализации бизнес-логики, связанной с проверкой решений и получением возможной награды за задачу.
"""

from typing import Protocol

from backend.core.schemas.submission import SubmissionId, SubmissionCreateRequest


class ISubmissionService(Protocol):
    """
    Протокол (интерфейс) сервиса управления отправками решений.
    Описывает методы для работы с отправками решений, которые должны быть реализованы в сервисе.
    """

    async def check_submission(
            self,
            user_id: int,
            data: SubmissionCreateRequest,
    ) -> SubmissionId:
        """
        Проверить отправленное решение задачи.

        :param user_id: Идентификатор пользователя (участника).
        :param data: todo
        :return: Объект с идентификатором отправки решения.
        """
        ...
