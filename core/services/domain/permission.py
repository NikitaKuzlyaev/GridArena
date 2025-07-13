from datetime import datetime
from typing import Sequence, Optional, Callable, Awaitable

# from core.dependencies.repository import get_repository, get_repository_manual
from core.models import Contest
from core.models.permission import PermissionResourceType, PermissionActionType, Permission
from core.repository.crud.contest import ContestCRUDRepository
from core.repository.crud.permission import PermissionCRUDRepository
from core.schemas.contest import ContestId, ContestShortInfo
from core.schemas.permission import PermissionId

from core.services.interfaces.contest import IContestService
from core.services.interfaces.permission import IPermissionService
from core.utilities.exceptions.database import EntityDoesNotExist
from core.utilities.exceptions.permission import PermissionDenied
from core.utilities.loggers.log_decorator import log_calls


class PermissionService(IPermissionService):
    def __init__(
            self,
            permission_repo: PermissionCRUDRepository,

    ):
        self.permission_repo = permission_repo

    async def raise_if_not_all(
            self,
            permissions: list[Callable[[], Awaitable[Permission | None]]],
    ) -> None:
        for permission in permissions:
            result = await permission()
            if result is None:
                raise PermissionDenied('Permission denied')

    async def create_permission(
            self,
            user_id: int,
            resource_type: str,
            permission_type: str,
            resource_id: Optional[int] = None,
    ) -> PermissionId:
        permission: Permission = (
            await self.permission_repo.create_permission(
                user_id=user_id,
                resource_type=resource_type,
                resource_id=resource_id,
                permission_type=permission_type,
            )
        )
        res = PermissionId(permission_id=permission.id)
        return res

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
        permission: Permission = (
            await self.permission_repo.check_permission(
                user_id=user_id,
                resource_type=resource_type,
                resource_id=resource_id,
                permission_type=permission_type,
            )
        )
        if not permission:
            return None
        res = PermissionId(permission_id=permission.id)
        return res

    async def give_permission_for_admin_contest(
            self,
            user_id: int,
            contest_id: int,
    ) -> PermissionId:
        res: PermissionId = await self.create_permission(
            user_id=user_id,
            resource_type=PermissionResourceType.CONTEST.value,
            permission_type=PermissionActionType.ADMIN.value,
            resource_id=contest_id,
        )
        return res

    async def give_permission_for_edit_contest(
            self,
            user_id: int,
            contest_id: int,
    ) -> PermissionId:
        res: PermissionId = await self.create_permission(
            user_id=user_id,
            resource_type=PermissionResourceType.CONTEST.value,
            permission_type=PermissionActionType.EDIT.value,
            resource_id=contest_id,
        )
        return res
