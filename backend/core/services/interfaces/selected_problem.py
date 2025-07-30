"""
Интерфейс сервиса для работы с выбранными (купленными пользователями) задачами.

Определяет контракт для реализации бизнес-логики, связанной с получением и покупкой выбранных задач участниками.
"""

from typing import Protocol

from backend.core.schemas.selected_problem import (
    SelectedProblemId,
    ArraySelectedProblemInfoForContestant,
)


class ISelectedProblemService(Protocol):
    """
    Протокол (интерфейс) сервиса управления выбранными задачами.
    Описывает методы для работы с выбранными задачами, которые должны быть реализованы в сервисе.
    """

    async def get_contestant_selected_problems(
            self,
            user_id: int,
    ) -> ArraySelectedProblemInfoForContestant:
        """
        Получить список выбранных задач участника.

        :param user_id: Идентификатор пользователя (участника).
        :return: Список информации о выбранных задачах участника.
        """
        ...

    async def buy_selected_problem(
            self,
            user_id: int,
            selected_problem_id: int,
    ) -> SelectedProblemId:
        """
        Купить выбранную задачу (открыть задачу для решения).

        :param user_id: Идентификатор пользователя (участника).
        :param selected_problem_id: Идентификатор выбранной задачи.
        :return: Объект с идентификатором выбранной задачи.
        """
        ...
