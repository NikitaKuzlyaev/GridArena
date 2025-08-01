"""
Интерфейс сервиса для работы с карточками задач.

Определяет контракт для реализации бизнес-логики, связанной с созданием,
обновлением и получением информации о карточках задач, а также их привязкой к полям и задачам.
"""

from typing import Protocol

from backend.core.schemas.problem_card import (
    ProblemCardId,
    ProblemCardInfoForEditor,
)


class IProblemCardService(Protocol):
    """
    Протокол (интерфейс) сервиса управления карточками задач.
    Описывает методы для работы с карточками задач, которые должны быть реализованы в сервисе.
    """

    async def create_problem_card_with_problem(
            self,
            user_id: int,
            quiz_field_id: int,
            row: int,
            column: int,
            category_name: str,
            category_price: int,
            statement: str,
            answer: str,
    ) -> ProblemCardId:
        """
        Создать новую карточку задачи и задачу одновременно.

        :param user_id: Идентификатор пользователя (редактора).
        :param quiz_field_id: Идентификатор поля.
        :param row: Номер строки на поле.
        :param column: Номер столбца на поле.
        :param category_name: Название категории.
        :param category_price: Цена категории (баллы).
        :param statement: Условие задачи.
        :param answer: Ответ на задачу.
        :return: Объект с идентификатором созданной карточки задачи.
        """
        ...

    async def update_problem_card_with_problem(
            self,
            user_id: int,
            problem_card_id: int,
            problem_id: int,
            category_name: str,
            category_price: int,
            statement: str,
            answer: str,
    ) -> ProblemCardId:
        """
        Обновить карточку задачи и связанную с ней задачу.

        :param user_id: Идентификатор пользователя (редактора).
        :param problem_card_id: Идентификатор карточки задачи.
        :param problem_id: Идентификатор задачи.
        :param category_name: Новое название категории.
        :param category_price: Новая цена категории.
        :param statement: Новое условие задачи.
        :param answer: Новый ответ на задачу.
        :return: Объект с идентификатором обновлённой карточки задачи.
        """
        ...

    async def create_problem_card(
            self,
            user_id: int,
            problem_id: int,
            category_name: str,
            category_price: int,
            quiz_field_id: int,
            row: int,
            column: int,
    ) -> ProblemCardId:
        """
        Создать новую карточку задачи для существующей задачи.

        :param user_id: Идентификатор пользователя (редактора).
        :param problem_id: Идентификатор задачи.
        :param category_name: Название категории.
        :param category_price: Цена категории (баллы).
        :param quiz_field_id: Идентификатор поля.
        :param row: Номер строки на поле.
        :param column: Номер столбца на поле.
        :return: Объект с идентификатором созданной карточки задачи.
        """
        ...

    async def update_problem_card(
            self,
            user_id: int,
            problem_card_id: int,
            category_name: str,
            category_price: int,
    ) -> ProblemCardId:
        """
        Обновить параметры карточки задачи.

        :param user_id: Идентификатор пользователя (редактора).
        :param problem_card_id: Идентификатор карточки задачи.
        :param category_name: Новое название категории.
        :param category_price: Новая цена категории.
        :return: Объект с идентификатором обновлённой карточки задачи.
        """
        ...

    async def problem_card_info_for_editor(
            self,
            user_id: int,
            problem_card_id: int,
    ) -> ProblemCardInfoForEditor:
        """
        Получить подробную информацию о карточке задачи для редактора.

        :param user_id: Идентификатор пользователя (редактора).
        :param problem_card_id: Идентификатор карточки задачи.
        :return: Подробная информация о карточке задачи для редактора.
        """
        ...
