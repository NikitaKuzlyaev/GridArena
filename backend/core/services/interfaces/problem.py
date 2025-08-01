"""
Интерфейс сервиса для работы с задачами.

Определяет контракт для реализации бизнес-логики, связанной с созданием и обновлением задач.
"""

from typing import Protocol

from backend.core.schemas.problem import ProblemId


class IProblemService(Protocol):
    """
    Протокол (интерфейс) сервиса управления задачами.
    Описывает методы для работы с задачами, которые должны быть реализованы в сервисе.
    """

    async def create_problem(
            self,
            user_id: int,
            statement: str,
            answer: str,
    ) -> ProblemId:
        """
        Создать новую задачу.

        :param user_id: Идентификатор пользователя.
        :param statement: Условие задачи.
        :param answer: Ответ на задачу.
        :return: Объект с идентификатором созданной задачи.
        """
        ...

    async def update_problem(
            self,
            user_id: int,
            problem_id: int,
            statement: str,
            answer: str,
    ) -> ProblemId:
        """
        Обновить существующую задачу.

        :param user_id: Идентификатор пользователя.
        :param problem_id: Идентификатор задачи.
        :param statement: Новое условие задачи.
        :param answer: Новый ответ на задачу.
        :return: Объект с идентификатором обновлённой задачи.
        """
        ...
