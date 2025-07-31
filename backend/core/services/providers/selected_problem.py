from fastapi import Depends

from backend.core.repository.crud.uow import (
    UnitOfWork,
    get_unit_of_work,
)
from backend.core.services.domain.selected_problem import SelectedProblemService
from backend.core.services.interfaces.selected_problem import ISelectedProblemService


def get_selected_problem_service(
        uow: UnitOfWork = Depends(get_unit_of_work),
) -> ISelectedProblemService:
    return SelectedProblemService(
        uow=uow,
    )
