"""
Интерфейс сервиса для работы с контестами.

Определяет контракт для реализации бизнес-логики, связанной с созданием, обновлением,
удалением и получением информации о контестах, а также получения результатов и отправленных решений.
"""
from datetime import datetime
from typing import Protocol

from backend.core.schemas.contest import (
    ContestId,
    ContestInfoForEditor,
    ContestInfoForContestant,
    ArrayContestShortInfo,
    ContestStandings,
    ContestSubmissions,
)


class IContestService(Protocol):
    """
    Протокол (интерфейс) сервиса управления контестами.
    Описывает методы для работы с контестами, которые должны быть реализованы в сервисе.
    """

    async def contest_submissions(
            self,
            contest_id: int,
    ) -> ContestSubmissions:
        """
        Получить все отправленные решения для указанного контеста.

        :param contest_id: Идентификатор контеста.
        :return: Объект с информацией о решениях в контесте.
        """
        ...

    async def contest_standings(
            self,
            contest_id: int,
    ) -> ContestStandings:
        """
        Получить турнирную таблицу (статистику) по контесту.

        :param contest_id: Идентификатор контеста.
        :return: Объект с турнирной таблицей контеста.
        """
        ...

    async def create_full_contest(
            self,
            user_id: int,
            name: str,
            started_at: datetime,
            closed_at: datetime,
            start_points: int,
            number_of_slots_for_problems: int,
    ) -> ContestId:
        """
        Создать новый контест с полным набором параметров.

        :param user_id: Идентификатор пользователя (создателя).
        :param name: Название контеста.
        :param started_at: Дата и время начала контеста.
        :param closed_at: Дата и время окончания контеста.
        :param start_points: Стартовое количество баллов.
        :param number_of_slots_for_problems: Количество слотов для задач.
        :return: Объект с идентификатором созданного контеста.
        """
        ...

    async def contest_info_for_contestant(
            self,
            user_id,
            contest_id,
    ) -> ContestInfoForContestant:
        """
        Получить информацию о контесте для участника.

        :param user_id: Идентификатор пользователя (участника).
        :param contest_id: Идентификатор контеста.
        :return: Информация о контеста для участника.
        """
        ...

    async def delete_contest(
            self,
            user_id,
            contest_id,
    ) -> None:
        """
        Удалить контест.

        :param user_id: Идентификатор пользователя (инициатора удаления).
        :param contest_id: Идентификатор контеста.
        """
        ...

    async def contest_info_for_editor(
            self,
            user_id,
            contest_id,
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
            name: str,
            started_at: datetime,
            closed_at: datetime,
            start_points: int,
            number_of_slots_for_problems: int,
    ) -> ContestId:
        """
        Создать новый контест (базовая версия).

        :param user_id: Идентификатор пользователя (создателя).
        :param name: Название контеста.
        :param started_at: Дата и время начала контеста.
        :param closed_at: Дата и время окончания контеста.
        :param start_points: Стартовое количество баллов.
        :param number_of_slots_for_problems: Количество слотов для задач.
        :return: Объект с идентификатором созданного контеста.
        """
        ...

    async def update_contest(
            self,
            user_id: int,
            contest_id: int,
            name: str,
            started_at: datetime,
            closed_at: datetime,
            start_points: int,
            number_of_slots_for_problems: int,
            rule_type: str,
            flag_user_can_have_negative_points: bool,
    ) -> ContestId:
        """
        Обновить параметры контеста.

        :param user_id: Идентификатор пользователя (инициатора обновления).
        :param contest_id: Идентификатор контеста.
        :param name: Новое название контеста.
        :param started_at: Новое время начала.
        :param closed_at: Новое время окончания.
        :param start_points: Новое стартовое количество баллов.
        :param number_of_slots_for_problems: Новое количество слотов для задач.
        :param rule_type: Тип правил контеста.
        :param flag_user_can_have_negative_points: Флаг, разрешающий отрицательные баллы у участников.
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
