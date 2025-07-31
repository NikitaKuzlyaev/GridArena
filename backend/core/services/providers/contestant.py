from fastapi import Depends

from backend.core.repository.crud.uow import (
    UnitOfWork,
    get_unit_of_work,
)
from backend.core.services.domain.contestant import ContestantService
from backend.core.services.interfaces.contestant import IContestantService
from backend.core.services.interfaces.permission import IPermissionService
from backend.core.services.providers.permission import get_permission_service
from backend.core.utilities.loggers.log_decorator import log_calls


@log_calls
def get_contestant_service(
        uow: UnitOfWork = Depends(get_unit_of_work),
        #permission_service: IPermissionService = Depends(get_permission_service),
) -> IContestantService:
    return ContestantService(
        uow=uow,
        #permission_service=permission_service,
    )
