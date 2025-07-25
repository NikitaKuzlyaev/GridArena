from fastapi import Depends

from backend.core.dependencies.repository import get_repository
from backend.core.repository.crud.contest import ContestCRUDRepository
from backend.core.repository.crud.contestant import ContestantCRUDRepository
from backend.core.repository.crud.problem_card import ProblemCardCRUDRepository
from backend.core.repository.crud.quiz import QuizFieldCRUDRepository
from backend.core.repository.crud.selected_problem import SelectedProblemCRUDRepository
from backend.core.repository.crud.user import UserCRUDRepository
from backend.core.services.domain.quiz import QuizFieldService
from backend.core.services.interfaces.quiz import IQuizFieldService


def get_quiz_field_service(
        quiz_repo: QuizFieldCRUDRepository = Depends(get_repository(QuizFieldCRUDRepository)),
        problem_card_repo: ProblemCardCRUDRepository = Depends(get_repository(ProblemCardCRUDRepository)),
        contestant_repo: ContestantCRUDRepository = Depends(get_repository(ContestantCRUDRepository)),
        user_repo: UserCRUDRepository = Depends(get_repository(UserCRUDRepository)),
        selected_problem_repo: SelectedProblemCRUDRepository = Depends(get_repository(SelectedProblemCRUDRepository)),
        contest_repo: ContestCRUDRepository = Depends(get_repository(ContestCRUDRepository)),
) -> IQuizFieldService:
    return QuizFieldService(
        quiz_field_repo=quiz_repo,
        problem_card_repo=problem_card_repo,
        contestant_repo=contestant_repo,
        user_repo=user_repo,
        selected_problem_repo=selected_problem_repo,
        contest_repo=contest_repo,
    )
