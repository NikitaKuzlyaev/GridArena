from sqlalchemy import select

from backend.core.models.permission import (
    Permission,
    PermissionActionType,
    PermissionResourceType,
)
from backend.core.repository.crud.base import BaseCRUDRepository
from backend.core.utilities.loggers.log_decorator import log_calls


class PermissionCRUDRepository(BaseCRUDRepository):

    @log_calls
    async def check_permission(
            self,
            user_id: int,
            resource_type: str,
            permission_type: str,
            resource_id: int,
    ) -> Permission | None:
        permission = await self.async_session.execute(
            select(Permission)
            .where(
                Permission.user_id == user_id,
                Permission.resource_type == resource_type,
                Permission.resource_id == resource_id,
                Permission.permission_type == permission_type
            )
        )
        return permission.scalar_one_or_none()

    @log_calls
    async def create_permission(
            self,
            user_id: int,
            resource_type: str,
            permission_type: str,
            resource_id: int,
    ) -> Permission:
        permission: Permission | None = (
            await self.check_permission(
                user_id=user_id,
                resource_type=resource_type,
                resource_id=resource_id,
                permission_type=permission_type,
            )
        )
        if permission:
            return permission

        permission = Permission(
            user_id=user_id,
            resource_type=PermissionResourceType(resource_type),
            resource_id=resource_id,
            permission_type=PermissionActionType(permission_type),
        )
        self.async_session.add(instance=permission)
        await self.async_session.flush()
        # await self.async_session.commit()
        # await self.async_session.refresh(instance=permission)
        return permission


"""
Пример вызова

permission_repo = get_repository(
    repo_type=PermissionCRUDRepository
)
"""
