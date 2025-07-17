from fastapi import Depends

from core.dependencies.repository import get_repository
from core.repository.crud.problem_card import ProblemCardCRUDRepository
from core.repository.crud.quiz import QuizFieldCRUDRepository
from core.services.domain.quiz import QuizFieldService
from core.services.interfaces.quiz import IQuizFieldService


def get_quiz_field_service(
        quiz_repo: QuizFieldCRUDRepository = Depends(get_repository(QuizFieldCRUDRepository)),
        problem_card_repo: ProblemCardCRUDRepository = Depends(get_repository(ProblemCardCRUDRepository)),
) -> IQuizFieldService:
    return QuizFieldService(
        quiz_field_repo=quiz_repo,
        problem_card_repo=problem_card_repo,
    )
