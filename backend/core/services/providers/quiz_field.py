from fastapi import Depends

from backend.core.repository.crud.uow import (
    UnitOfWork,
    get_unit_of_work,
)
from backend.core.services.domain.quiz_field import QuizFieldService
from backend.core.services.interfaces.quiz_field import IQuizFieldService


def get_quiz_field_service(
        uow: UnitOfWork = Depends(get_unit_of_work),
) -> IQuizFieldService:
    return QuizFieldService(
        uow=uow,
    )
