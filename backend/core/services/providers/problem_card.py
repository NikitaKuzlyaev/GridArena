from fastapi import Depends

from backend.core.dependencies.repository import get_repository
from backend.core.repository.crud.problem_card import ProblemCardCRUDRepository
from backend.core.repository.crud.quiz import QuizFieldCRUDRepository
from backend.core.services.domain.problem_card import ProblemCardService
from backend.core.services.interfaces.problem_card import IProblemCardService


def get_problem_card_service(
        problem_card_repo: ProblemCardCRUDRepository = Depends(get_repository(ProblemCardCRUDRepository)),
        quiz_field_repo: QuizFieldCRUDRepository = Depends(get_repository(QuizFieldCRUDRepository)),
) -> IProblemCardService:
    return ProblemCardService(
        problem_card_repo=problem_card_repo,
        quiz_field_repo=quiz_field_repo,
    )
