from datetime import datetime
from typing import Protocol, Optional, Callable, Awaitable
from typing import Sequence

from core.models import Contest, Permission
from core.models.permission import PermissionActionType, PermissionResourceType

from core.schemas.contest import ContestId, ContestCreateRequest, ContestShortInfo
from core.schemas.permission import PermissionId
from core.utilities.exceptions.permission import PermissionDenied


class IPermissionService(Protocol):

    async def raise_if_not_all(
            self,
            permissions: list[Callable[[], Awaitable[int | None]]],
    ) -> None:
        ...

    async def create_permission(
            self,
            user_id: int,
            resource_type: str,
            permission_type: str,
            resource_id: Optional[int] = None,
    ) -> PermissionId:
        ...

    async def delete_permission(
            self,
            user_id: int,
            resource_type: str,
            permission_type: str,
            resource_id: Optional[int] = None,
    ) -> None:
        ...

    async def check_permission(
            self,
            user_id: int,
            resource_type: str,
            permission_type: str,
            resource_id: Optional[int] = None,
    ) -> PermissionId | None:
        ...

    async def give_permission_for_admin_contest(
            self,
            user_id: int,
            contest_id: int,
    ) -> PermissionId:
        ...

    async def check_permission_for_admin_contest(
            self,
            user_id: int,
            contest_id: int,
    ) -> PermissionId | None:
        ...

    async def give_permission_for_edit_contest(
            self,
            user_id: int,
            contest_id: int,
    ) -> PermissionId:
        ...

    async def check_permission_for_edit_contest(
            self,
            user_id: int,
            contest_id: int,
    ) -> PermissionId | None:
        ...

    async def check_permission_for_edit_quiz_field(
            self,
            user_id: int,
            quiz_field_id: int,
    ) -> PermissionId | None:
        ...

    async def check_permission_for_edit_problem_card(
            self,
            user_id: int,
            problem_card_id: int,
    ) -> PermissionId | None:
        ...

    async def check_permission_for_edit_problem(
            self,
            user_id: int,
            problem_id: int,
    ) -> PermissionId | None:
        ...