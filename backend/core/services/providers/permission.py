from fastapi import Depends

from backend.core.repository.crud.uow import (
    UnitOfWork,
    get_unit_of_work,
)
from backend.core.services.domain.permission import PermissionService
from backend.core.services.interfaces.permission import IPermissionService


def get_permission_service(
        uow: UnitOfWork = Depends(get_unit_of_work),
) -> IPermissionService:
    return PermissionService(
        uow=uow,
    )
