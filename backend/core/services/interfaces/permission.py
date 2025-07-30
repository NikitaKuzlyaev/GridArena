"""
Интерфейс сервиса для работы с правами доступа.

Определяет контракт для реализации бизнес-логики, связанной с управлением правами доступа
пользователей к различным ресурсам системы (контесты, задачи, поля и т.д.).
"""

from typing import Protocol, Optional, Callable, Awaitable

from backend.core.schemas.permission import PermissionId, PermissionPromise


class IPermissionService(Protocol):
    """
    Протокол (интерфейс) сервиса управления правами доступа.
    Описывает методы для работы с правами доступа, которые должны быть реализованы в сервисе.
    """

    async def raise_if_not_all(
            self,
            permissions: list[Callable[[], Awaitable[int | None]]],
    ) -> None:
        """
        Проверить все переданные разрешения и выбросить исключение, если хотя бы одно не выполнено.

        :param permissions: Список функций-проверок разрешений, возвращающих ID разрешения или None.
        """
        ...

    async def create_permission(
            self,
            user_id: int,
            resource_type: str,
            permission_type: str,
            resource_id: Optional[int] = None,
    ) -> PermissionId:
        """
        Создать новое разрешение для пользователя.

        :param user_id: Идентификатор пользователя.
        :param resource_type: Тип ресурса (например, 'contest', 'problem', 'quiz_field').
        :param permission_type: Тип разрешения (например, 'admin', 'edit', 'view').
        :param resource_id: Идентификатор конкретного ресурса (опционально).
        :return: Объект с идентификатором созданного разрешения.
        """
        ...

    async def delete_permission(
            self,
            user_id: int,
            resource_type: str,
            permission_type: str,
            resource_id: Optional[int] = None,
    ) -> None:
        """
        Удалить разрешение пользователя.

        :param user_id: Идентификатор пользователя.
        :param resource_type: Тип ресурса.
        :param permission_type: Тип разрешения.
        :param resource_id: Идентификатор конкретного ресурса (опционально).
        """
        ...

    async def check_permission(
            self,
            user_id: int,
            resource_type: str,
            permission_type: str,
            resource_id: Optional[int] = None,
    ) -> PermissionId | None:
        """
        Проверить наличие разрешения у пользователя.

        :param user_id: Идентификатор пользователя.
        :param resource_type: Тип ресурса.
        :param permission_type: Тип разрешения.
        :param resource_id: Идентификатор конкретного ресурса (опционально).
        :return: ID разрешения, если оно существует, иначе None.
        """
        ...

    async def give_permission_for_admin_contest(
            self,
            user_id: int,
            contest_id: int,
    ) -> PermissionId:
        """
        Предоставить пользователю права администратора контеста.

        :param user_id: Идентификатор пользователя.
        :param contest_id: Идентификатор контеста.
        :return: Объект с идентификатором созданного разрешения.
        """
        ...

    async def check_permission_for_admin_contest(
            self,
            user_id: int,
            contest_id: int,
    ) -> PermissionId | None:
        """
        Проверить наличие прав администратора контеста у пользователя.

        :param user_id: Идентификатор пользователя.
        :param contest_id: Идентификатор контеста.
        :return: ID разрешения, если оно существует, иначе None.
        """
        ...

    async def give_permission_for_edit_contest(
            self,
            user_id: int,
            contest_id: int,
    ) -> PermissionId:
        """
        Предоставить пользователю права редактирования контеста.

        :param user_id: Идентификатор пользователя.
        :param contest_id: Идентификатор контеста.
        :return: Объект с идентификатором созданного разрешения.
        """
        ...

    async def check_permission_for_edit_contest(
            self,
            user_id: int,
            contest_id: int,
    ) -> PermissionId | None:
        """
        Проверить наличие прав редактирования контеста у пользователя.

        :param user_id: Идентификатор пользователя.
        :param contest_id: Идентификатор контеста.
        :return: ID разрешения, если оно существует, иначе None.
        """
        ...

    async def check_permission_for_edit_quiz_field(
            self,
            user_id: int,
            quiz_field_id: int,
    ) -> PermissionId | None:
        """
        Проверить наличие прав редактирования поля у пользователя.

        :param user_id: Идентификатор пользователя.
        :param quiz_field_id: Идентификатор поля.
        :return: ID разрешения, если оно существует, иначе None.
        """
        ...

    async def check_permission_for_edit_problem_card(
            self,
            user_id: int,
            problem_card_id: int,
    ) -> PermissionId | None:
        """
        Проверить наличие прав редактирования карточки задачи у пользователя.

        :param user_id: Идентификатор пользователя.
        :param problem_card_id: Идентификатор карточки задачи.
        :return: ID разрешения, если оно существует, иначе None.
        """
        ...

    async def check_permission_for_edit_problem(
            self,
            user_id: int,
            problem_id: int,
    ) -> PermissionId | None:
        """
        Проверить наличие прав редактирования задачи у пользователя.

        :param user_id: Идентификатор пользователя.
        :param problem_id: Идентификатор задачи.
        :return: ID разрешения, если оно существует, иначе None.
        """
        ...

    async def check_permission_for_view_contest_standings(
            self,
            user_id: int,
            contest_id: int,
    ) -> PermissionPromise | None:
        """
        Проверить наличие прав просмотра турнирной таблицы контеста у пользователя.

        :param user_id: Идентификатор пользователя.
        :param contest_id: Идентификатор контеста.
        :return: Объект с сообщением о разрешении, если оно существует, иначе None.
        """
        ...
