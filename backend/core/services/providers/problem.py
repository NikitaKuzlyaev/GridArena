from fastapi import Depends

from backend.core.repository.crud.uow import (
    UnitOfWork,
    get_unit_of_work,
)
from backend.core.services.domain.problem import ProblemService
from backend.core.services.interfaces.problem import IProblemService


def get_problem_service(
        uow: UnitOfWork = Depends(get_unit_of_work),
) -> IProblemService:
    return ProblemService(
        uow=uow,
    )
