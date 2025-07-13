from datetime import datetime
from typing import Protocol, Optional
from typing import Sequence

from core.models import Contest, Permission
from core.models.permission import PermissionActionType, PermissionResourceType

from core.schemas.contest import ContestId, ContestCreateRequest, ContestShortInfo
from core.schemas.permission import PermissionId


class IPermissionService(Protocol):

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

    async def give_permission_for_edit_contest(
            self,
            user_id: int,
            contest_id: int,
    ) -> PermissionId:
        ...