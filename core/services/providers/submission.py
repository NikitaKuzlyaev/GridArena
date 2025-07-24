from fastapi import Depends

from core.dependencies.repository import get_repository
from core.repository.crud.contest import ContestCRUDRepository
from core.repository.crud.contestant import ContestantCRUDRepository
from core.repository.crud.problem import ProblemCRUDRepository
from core.repository.crud.problem_card import ProblemCardCRUDRepository
from core.repository.crud.quiz import QuizFieldCRUDRepository
from core.repository.crud.selected_problem import SelectedProblemCRUDRepository
from core.repository.crud.submission import SubmissionCRUDRepository
from core.repository.crud.transaction import TransactionCRUDRepository
from core.repository.crud.user import UserCRUDRepository
from core.services.domain.submission import SubmissionService
from core.services.interfaces.submission import ISubmissionService


def get_submission_service(
        submission_repo: SubmissionCRUDRepository = Depends(get_repository(SubmissionCRUDRepository)),
        selected_problem_repo: SelectedProblemCRUDRepository = Depends(get_repository(SelectedProblemCRUDRepository)),
        problem_card_repo: ProblemCardCRUDRepository = Depends(get_repository(ProblemCardCRUDRepository)),
        contestant_repo: ContestantCRUDRepository = Depends(get_repository(ContestantCRUDRepository)),
        user_repo: UserCRUDRepository = Depends(get_repository(UserCRUDRepository)),
        transaction_repo: TransactionCRUDRepository = Depends(get_repository(TransactionCRUDRepository)),
        contest_repo: ContestCRUDRepository = Depends(get_repository(ContestCRUDRepository)),
        problem_repo: ProblemCRUDRepository = Depends(get_repository(ProblemCRUDRepository)),
        quiz_field_repo: QuizFieldCRUDRepository = Depends(get_repository(QuizFieldCRUDRepository)),
) -> ISubmissionService:
    return SubmissionService(
        submission_repo=submission_repo,
        selected_problem_repo=selected_problem_repo,
        problem_card_repo=problem_card_repo,
        contestant_repo=contestant_repo,
        user_repo=user_repo,
        transaction_repo=transaction_repo,
        contest_repo=contest_repo,
        problem_repo=problem_repo,
        quiz_field_repo=quiz_field_repo,
    )
