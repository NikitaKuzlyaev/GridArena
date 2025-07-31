from fastapi import Depends

from backend.core.repository.crud.uow import (
    UnitOfWork,
    get_unit_of_work,
)
from backend.core.services.domain.problem_card import ProblemCardService
from backend.core.services.interfaces.problem_card import IProblemCardService


def get_problem_card_service(
        uow: UnitOfWork = Depends(get_unit_of_work),
) -> IProblemCardService:
    return ProblemCardService(
        uow=uow,
    )
