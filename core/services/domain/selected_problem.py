from typing import Sequence, Tuple

from core.models import Contestant, User, SelectedProblem, ProblemCard, Problem, Contest
from core.models.selected_problem import SelectedProblemStatusType
from core.repository.crud.contest import ContestCRUDRepository
from core.repository.crud.contestant import ContestantCRUDRepository
from core.repository.crud.problem_card import ProblemCardCRUDRepository
from core.repository.crud.selected_problem import SelectedProblemCRUDRepository
from core.repository.crud.transaction import TransactionCRUDRepository
from core.repository.crud.user import UserCRUDRepository
from core.schemas.problem import ProblemInfoForContestant
from core.schemas.selected_problem import SelectedProblemId, SelectedProblemInfoForContestant, \
    ArraySelectedProblemInfoForContestant
from core.services.interfaces.selected_problem import ISelectedProblemService
from core.utilities.exceptions.database import EntityDoesNotExist, EntityAlreadyExists
from core.utilities.exceptions.logic import PossibleLimitOverflow
from core.utilities.loggers.log_decorator import log_calls


class SelectedProblemService(ISelectedProblemService):
    def __init__(
            self,
            selected_problem_repo: SelectedProblemCRUDRepository,
            problem_card_repo: ProblemCardCRUDRepository,
            contestant_repo: ContestantCRUDRepository,
            user_repo: UserCRUDRepository,
            transaction_repo: TransactionCRUDRepository,
            contest_repo: ContestCRUDRepository,
    ):
        self.selected_problem_repo = selected_problem_repo
        self.problem_card_repo = problem_card_repo
        self.contestant_repo = contestant_repo
        self.user_repo = user_repo
        self.transaction_repo = transaction_repo
        self.contest_repo = contest_repo

    @log_calls
    async def get_contestant_selected_problems(
            self,
            user_id: int,
    ) -> ArraySelectedProblemInfoForContestant:
        contestant: Contestant | None = (
            await self.contestant_repo.get_contestant_by_user_id(
                user_id=user_id,
            )
        )
        if not contestant:
            raise EntityDoesNotExist("contestant not found")

        rows: Sequence[Tuple[SelectedProblem, ProblemCard, Problem]] = (
            await self.selected_problem_repo.get_selected_problem_with_problem_card_and_problem_of_contestant_by_id(
                contestant_id=contestant.id,
            )
        )

        res = ArraySelectedProblemInfoForContestant(
            body=[
                SelectedProblemInfoForContestant(
                    selected_problem_id=selected_problem.id,
                    problem_card_id=problem_card.id,
                    problem=ProblemInfoForContestant(
                        problem_id=problem.id,
                        statement=problem.statement,
                    ),
                    created_at=selected_problem.created_at,
                ) for selected_problem, problem_card, problem in rows if
                selected_problem.status == SelectedProblemStatusType.ACTIVE
            ]
        )

        return res

    @log_calls
    async def buy_selected_problem(
            self,
            user_id: int,
            problem_card_id: int,
    ) -> SelectedProblemId:
        user: User = (
            await self.user_repo.get_user_by_id(
                user_id=user_id,
            )
        )
        if not user:
            raise EntityDoesNotExist("user not found")

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

        contest: Contest = (
            await self.contest_repo.get_contest_by_id(
                contest_id=user.domain_number
            )
        )
        active_selected_problems: Sequence[SelectedProblem] = (
            await self.selected_problem_repo.get_selected_problem_of_contestant_by_id(
                contestant_id=contestant.id,
                filter_by_status=[SelectedProblemStatusType.ACTIVE.value],
            )
        )
        if len(active_selected_problems) >= contest.number_of_slots_for_problems:
            raise PossibleLimitOverflow("")

        try:
            selected_problem: SelectedProblem = (
                await self.transaction_repo.buy_problem(
                    contestant_id=contestant.id,
                    problem_card_id=problem_card.id,
                )
            )
            res = SelectedProblemId(
                selected_problem_id=selected_problem.id,
            )
            return res

        except Exception as e:
            raise e
