"""
Интерфейс сервиса для работы с контестами.

Определяет контракт для реализации бизнес-логики, связанной с созданием, обновлением,
удалением и получением информации о контестах, а также получения результатов и отправленных решений.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from backend.core.schemas.contest import (
    ContestId,
    ContestInfoForEditor,
    ContestInfoForContestant,
    ArrayContestShortInfo,
    ContestStandings,
    ContestSubmissions, ContestCreateRequest, ContestUpdateRequest,
)
from backend.core.schemas.contestant import ContestantId, ContestantInCreate


class IContestService(Protocol):
    """
    Протокол (интерфейс) сервиса управления контестами.
    Описывает методы для работы с контестами, которые должны быть реализованы в сервисе.
    """

    async def contest_submissions(
            self,
            user_id: int,
            contest_id: int,
            show_user_only: bool,
    ) -> ContestSubmissions:
        """
        Получить все отправленные решения для указанного контеста.

        :param user_id: Идентификатор пользователя, совершающего операцию.
        :param contest_id: Идентификатор контеста.
        :param show_user_only: Флаг: отдавать только посылки пользователя (по умолчанию - нет).
        :return: Объект с информацией о решениях в контесте.
        """
        ...

    async def contest_standings(
            self,
            user_id: int,
            contest_id: int,
    ) -> ContestStandings:
        """
        Получить турнирную таблицу (статистику) по контесту.

        :param user_id: Идентификатор пользователя, совершающего операцию.
        :param contest_id: Идентификатор контеста.
        :return: Объект с турнирной таблицей контеста.
        """
        ...

    async def create_full_contest(
            self,
            user_id: int,
            contest_data: ContestCreateRequest,
    ) -> ContestId:
        """
        Создать новый контест с полным набором параметров.

        :param user_id: Идентификатор пользователя (создателя).
        :param contest_data: # todo.
        :return: Объект с идентификатором созданного контеста.
        """
        ...

    async def contest_info_for_contestant(
            self,
            user_id: int,
    ) -> ContestInfoForContestant:
        """
        Получить информацию о контесте для участника.

        :param user_id: Идентификатор пользователя (участника).
        :return: Информация о контеста для участника.
        """
        ...

    async def delete_contest(
            self,
            user_id: int,
            contest_id: int,
    ) -> None:
        """
        Удалить контест.

        :param user_id: Идентификатор пользователя (инициатора удаления).
        :param contest_id: Идентификатор контеста.
        """
        ...

    async def contest_info_for_editor(
            self,
            user_id: int,
            contest_id: int,
    ) -> ContestInfoForEditor:
        """
        Получить информацию о контесте для редактора (создателя/организатора).

        :param user_id: Идентификатор пользователя (редактора).
        :param contest_id: Идентификатор контеста.
        :return: Информация о контесте для редактора.
        """
        ...

    async def create_contest(
            self,
            user_id: int,
            contest_data: ContestCreateRequest,
    ) -> ContestId:
        """
        Создать новый контест (базовая версия).

        :param user_id: Идентификатор пользователя (создателя).
        :param contest_data: # todo
        :return: Объект с идентификатором созданного контеста.
        """
        ...

    async def update_contest(
            self,
            user_id: int,
            contest_data: ContestUpdateRequest,
    ) -> ContestId:
        """
        Обновить параметры контеста.

        :param user_id: Идентификатор пользователя (инициатора обновления).
        :param contest_data: # todo
        :return: Объект с идентификатором созданного контеста.
        """
        ...

    async def get_user_contests(
            self,
            user_id: int,
    ) -> ArrayContestShortInfo:
        """
        Получить список контестов, связанных с пользователем (где пользователь - редактор).

        :param user_id: Идентификатор пользователя.
        :return: Список краткой информации о контестах пользователя.
        """
        ...

    async def create_contestant(
            self,
            user_id: int,
            contestant_data: ContestantInCreate,
    ) -> ContestantId:
        """
        Получить список контестов, связанных с пользователем (где пользователь - редактор).

        :param user_id: Идентификатор пользователя (инициатора запроса).
        :param contestant_data: # todo
        :return: Объект с идентификатором нового пользователя.
        """
        ...
