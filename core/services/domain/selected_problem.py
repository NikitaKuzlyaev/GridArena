from core.models import Contestant, User, SelectedProblem, ProblemCard
from core.repository.crud.contestant import ContestantCRUDRepository
from core.repository.crud.problem_card import ProblemCardCRUDRepository
from core.repository.crud.selected_problem import SelectedProblemCRUDRepository
from core.repository.crud.user import UserCRUDRepository
from core.schemas.selected_problem import SelectedProblemId

from core.services.interfaces.selected_problem import ISelectedProblemService
from core.utilities.exceptions.database import EntityDoesNotExist, EntityAlreadyExists
from core.utilities.loggers.log_decorator import log_calls


class SelectedProblemService(ISelectedProblemService):
    def __init__(
            self,
            selected_problem_repo: SelectedProblemCRUDRepository,
            problem_card_repo: ProblemCardCRUDRepository,
            contestant_repo: ContestantCRUDRepository,
            user_repo: UserCRUDRepository,
    ):
        self.selected_problem_repo = selected_problem_repo
        self.problem_card_repo = problem_card_repo
        self.contestant_repo = contestant_repo
        self.user_repo = user_repo

    @log_calls
    async def buy_selected_problem(
            self,
            user_id: int,
            problem_card_id: int,
    ) -> SelectedProblemId:
        contestant: Contestant | None = (
            await self.contestant_repo.get_contestant_by_user_id(
                user_id=user_id,
            )
        )
        if not contestant:
            raise EntityDoesNotExist("contestant not found")

        problem_card: ProblemCard | None = (
            await self.problem_card_repo.get_problem_card_by_id(
                problem_card_id=problem_card_id,
            )
        )
        if not problem_card:
            raise EntityDoesNotExist("problem card not found")

        selected_problem: SelectedProblem | None = (
            await self.selected_problem_repo.get_selected_problem_by_contestant_and_problem_card(
                contestant_id=contestant.id,
                problem_card_id=problem_card_id,
            )
        )
        if selected_problem:
            raise EntityAlreadyExists("selected problem already exists")

        selected_problem: SelectedProblem = (
            await self.selected_problem_repo.create_selected_problem(
                contestant_id=contestant.id,
                problem_card_id=problem_card_id,
            )
        )
        res = SelectedProblemId(
            selected_problem_id=selected_problem.id,
        )

        return res
