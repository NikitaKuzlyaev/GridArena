"""
Интерфейс сервиса для работы с отправками решений.

Определяет контракт для реализации бизнес-логики, связанной с проверкой решений и получением возможной награды за задачу.
"""

from typing import Protocol

from backend.core.schemas.submission import (
    SubmissionId,
)


class ISubmissionService(Protocol):
    """
    Протокол (интерфейс) сервиса управления отправками решений.
    Описывает методы для работы с отправками решений, которые должны быть реализованы в сервисе.
    """

    async def check_submission(
            self,
            user_id: int,
            selected_problem_id: int,
            answer: str,
    ) -> SubmissionId:
        """
        Проверить отправленное решение задачи.

        :param user_id: Идентификатор пользователя (участника).
        :param selected_problem_id: Идентификатор выбранной задачи.
        :param answer: Ответ, отправленный пользователем.
        :return: Объект с идентификатором отправки решения.
        """
        ...

    async def get_possible_reward(
            self,
            selected_problem_id: int,
    ) -> int:
        """
        Получить возможную награду за выбранную задачу.

        :param selected_problem_id: Идентификатор выбранной задачи.
        :return: Возможная награда (баллы).
        """
        ...
