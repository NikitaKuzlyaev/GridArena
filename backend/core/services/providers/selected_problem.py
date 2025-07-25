from fastapi import Depends

from backend.core.dependencies.repository import get_repository
from backend.core.repository.crud.contest import ContestCRUDRepository
from backend.core.repository.crud.contestant import ContestantCRUDRepository
from backend.core.repository.crud.problem_card import ProblemCardCRUDRepository
from backend.core.repository.crud.selected_problem import SelectedProblemCRUDRepository
from backend.core.repository.crud.transaction import TransactionCRUDRepository
from backend.core.repository.crud.user import UserCRUDRepository
from backend.core.services.domain.selected_problem import SelectedProblemService
from backend.core.services.interfaces.selected_problem import ISelectedProblemService


def get_selected_problem_service(
        selected_problem_repo: SelectedProblemCRUDRepository = Depends(get_repository(SelectedProblemCRUDRepository)),
        problem_card_repo: ProblemCardCRUDRepository = Depends(get_repository(ProblemCardCRUDRepository)),
        contestant_repo: ContestantCRUDRepository = Depends(get_repository(ContestantCRUDRepository)),
        user_repo: UserCRUDRepository = Depends(get_repository(UserCRUDRepository)),
        transaction_repo: TransactionCRUDRepository = Depends(get_repository(TransactionCRUDRepository)),
        contest_repo: ContestCRUDRepository = Depends(get_repository(ContestCRUDRepository)),
) -> ISelectedProblemService:
    return SelectedProblemService(
        selected_problem_repo=selected_problem_repo,
        problem_card_repo=problem_card_repo,
        contestant_repo=contestant_repo,
        user_repo=user_repo,
        transaction_repo=transaction_repo,
        contest_repo=contest_repo,
    )
