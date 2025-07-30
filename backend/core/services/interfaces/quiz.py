"""
Интерфейс сервиса для работы с полями.

Определяет контракт для реализации бизнес-логики, связанной с созданием,
обновлением и получением информации о полях, а также их привязкой к контестам.
"""

from typing import Protocol

from backend.core.schemas.quiz_field import (
    QuizFieldId,
    QuizFieldInfoForEditor,
    QuizFieldInfoForContestant,
)


class IQuizFieldService(Protocol):
    """
    Протокол (интерфейс) сервиса управления полями.
    Описывает методы для работы с полями, которые должны быть реализованы в сервисе.
    """

    async def quiz_field_info_for_contestant(
            self,
            user_id,
    ) -> QuizFieldInfoForContestant:
        """
        Получить информацию о поле для участника.

        :param user_id: Идентификатор пользователя (участника).
        :return: Информация о поле для участника.
        """
        ...

    async def quiz_field_info_for_editor(
            self,
            user_id,
            contest_id,
    ) -> QuizFieldInfoForEditor:
        """
        Получить информацию о поле для редактора.

        :param user_id: Идентификатор пользователя (редактора).
        :param contest_id: Идентификатор контеста.
        :return: Информация о поле для редактора.
        """
        ...

    async def create_quiz_field(
            self,
            contest_id: int,
            number_of_rows: int,
            number_of_columns: int,
    ) -> QuizFieldId:
        """
        Создать новое поле.

        :param contest_id: Идентификатор контеста.
        :param number_of_rows: Количество строк.
        :param number_of_columns: Количество столбцов.
        :return: Объект с идентификатором созданного поля.
        """
        ...

    async def update_quiz_field(
            self,
            quiz_field_id: int,
            number_of_rows: int,
            number_of_columns: int,
    ) -> QuizFieldId:
        """
        Обновить параметры поля.

        :param quiz_field_id: Идентификатор поля.
        :param number_of_rows: Новое количество строк.
        :param number_of_columns: Новое количество столбцов.
        :return: Объект с идентификатором обновлённого поля.
        """
        ...
