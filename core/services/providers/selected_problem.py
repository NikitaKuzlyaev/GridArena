from fastapi import Depends

from core.dependencies.repository import get_repository
from core.repository.crud.contestant import ContestantCRUDRepository
from core.repository.crud.problem_card import ProblemCardCRUDRepository
from core.repository.crud.selected_problem import SelectedProblemCRUDRepository
from core.repository.crud.transaction import TransactionCRUDRepository
from core.repository.crud.user import UserCRUDRepository
from core.services.domain.selected_problem import SelectedProblemService
from core.services.interfaces.selected_problem import ISelectedProblemService


def get_selected_problem_service(
        selected_problem_repo: SelectedProblemCRUDRepository = Depends(get_repository(SelectedProblemCRUDRepository)),
        problem_card_repo: ProblemCardCRUDRepository = Depends(get_repository(ProblemCardCRUDRepository)),
        contestant_repo: ContestantCRUDRepository = Depends(get_repository(ContestantCRUDRepository)),
        user_repo: UserCRUDRepository = Depends(get_repository(UserCRUDRepository)),
        transaction_repo: TransactionCRUDRepository = Depends(get_repository(TransactionCRUDRepository)),
) -> ISelectedProblemService:
    return SelectedProblemService(
        selected_problem_repo=selected_problem_repo,
        problem_card_repo=problem_card_repo,
        contestant_repo=contestant_repo,
        user_repo=user_repo,
        transaction_repo=transaction_repo,
    )
