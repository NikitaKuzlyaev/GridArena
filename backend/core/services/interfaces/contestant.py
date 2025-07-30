"""
Интерфейс сервиса для работы с участниками контестов.

Определяет контракт для реализации бизнес-логики, связанной с созданием участников,
получением информации об участниках и управлением их данными в рамках контестов.
"""

from typing import Protocol

from backend.core.schemas.contestant import (
    ArrayContestantInfoForEditor,
    ContestantId,
    ContestantPreviewInfo,
    ContestantInfoInContest,
)


class IContestantService(Protocol):
    """
    Протокол (интерфейс) сервиса управления участниками контестов.
    Описывает методы для работы с участниками, которые должны быть реализованы в сервисе.
    """

    async def get_contestant_info_in_contest(
            self,
            user_id: int,
    ) -> ContestantInfoInContest:
        """
        Получить информацию об участнике в рамках конкретного контеста.

        :param user_id: Идентификатор пользователя (участника).
        :return: Информация об участнике в контексте контеста.
        """
        ...

    async def get_contestant_preview(
            self,
            user_id: int,
    ) -> ContestantPreviewInfo:
        """
        Получить краткую информацию об участнике и его контесте.

        :param user_id: Идентификатор пользователя (участника).
        :return: Краткая информация об участнике и контесте.
        """
        ...

    async def get_contestants_in_contest(
            self,
            user_id: int,
            contest_id: int,
    ) -> ArrayContestantInfoForEditor:
        """
        Получить список всех участников в контесте (для редактора).

        :param user_id: Идентификатор пользователя (редактора).
        :param contest_id: Идентификатор контеста.
        :return: Список информации об участниках контеста.
        """
        ...

    async def create_contestant(
            self,
            contest_id: int,
            username: str,
            password: str,
            name: str,
            points: int,
    ) -> ContestantId:
        """
        Создать нового участника контеста.

        :param contest_id: Идентификатор контеста.
        :param username: Имя пользователя участника.
        :param password: Пароль участника.
        :param name: Отображаемое имя участника.
        :param points: Начальное количество баллов.
        :return: Объект с идентификатором созданного участника.
        """
        ...
