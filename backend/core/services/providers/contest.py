from fastapi import Depends

from backend.core.repository.crud.uow import (
    UnitOfWork,
    get_unit_of_work,
)
from backend.core.services.domain.contest import ContestService
from backend.core.services.interfaces.contest import IContestService
from backend.core.services.interfaces.permission import IPermissionService
from backend.core.services.providers.permission import get_permission_service


def get_contest_service(
        uow: UnitOfWork = Depends(get_unit_of_work),
        # permission_service: IPermissionService = Depends(get_permission_service),
) -> IContestService:
    return ContestService(
        uow=uow,
        # permission_service=permission_service,
    )
