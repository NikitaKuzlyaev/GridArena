from fastapi import Depends

from backend.core.repository.crud.uow import (
    UnitOfWork,
    get_unit_of_work,
)
from backend.core.services.domain.contest import ContestService
from backend.core.services.interfaces.contest import IContestService


def get_contest_service(
        uow: UnitOfWork = Depends(get_unit_of_work),
) -> IContestService:
    return ContestService(
        uow=uow,
    )
