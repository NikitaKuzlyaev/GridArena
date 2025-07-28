from typing import Sequence, Tuple

from backend.core.models import Contestant, User, SelectedProblem, ProblemCard, Problem, Contest
from backend.core.models.contest import ContestRuleType
from backend.core.models.selected_problem import SelectedProblemStatusType
from backend.core.models.submission import SubmissionVerdict
from backend.core.repository.crud.contest import ContestCRUDRepository
from backend.core.repository.crud.contestant import ContestantCRUDRepository
from backend.core.repository.crud.problem import ProblemCRUDRepository
from backend.core.repository.crud.problem_card import ProblemCardCRUDRepository
from backend.core.repository.crud.quiz import QuizFieldCRUDRepository
from backend.core.repository.crud.selected_problem import SelectedProblemCRUDRepository
from backend.core.repository.crud.submission import SubmissionCRUDRepository
from backend.core.repository.crud.transaction import TransactionCRUDRepository
from backend.core.repository.crud.user import UserCRUDRepository
from backend.core.schemas.problem import ProblemInfoForContestant
from backend.core.schemas.selected_problem import (
    SelectedProblemId, SelectedProblemInfoForContestant, ArraySelectedProblemInfoForContestant)
from backend.core.services.context.context import ContextService, RepositoryUnit, ContextModel
from backend.core.services.interfaces.selected_problem import ISelectedProblemService
from backend.core.utilities.exceptions.database import EntityAlreadyExists
from backend.core.utilities.exceptions.logic import PossibleLimitOverflow
from backend.core.utilities.loggers.log_decorator import log_calls

MAX_NUMBER_OF_ATTEMPTS = 3

class SelectedProblemService(ISelectedProblemService):
    def __init__(
            self,
            selected_problem_repo: SelectedProblemCRUDRepository,
            problem_card_repo: ProblemCardCRUDRepository,
            contestant_repo: ContestantCRUDRepository,
            user_repo: UserCRUDRepository,
            transaction_repo: TransactionCRUDRepository,
            contest_repo: ContestCRUDRepository,
            submission_repo: SubmissionCRUDRepository,
            problem_repo: ProblemCRUDRepository,
            quiz_field_repo: QuizFieldCRUDRepository,
    ):
        self.selected_problem_repo = selected_problem_repo
        self.problem_card_repo = problem_card_repo
        self.contestant_repo = contestant_repo
        self.user_repo = user_repo
        self.transaction_repo = transaction_repo
        self.contest_repo = contest_repo
        self.submission_repo = submission_repo
        self.problem_repo = problem_repo
        self.quiz_field_repo = quiz_field_repo
        self.context_service = ContextService(
            context=ContextModel(
                repository_unit=RepositoryUnit(
                    submission_repo=self.submission_repo,
                    selected_problem_repo=self.selected_problem_repo,
                    problem_card_repo=self.problem_card_repo,
                    contestant_repo=self.contestant_repo,
                    user_repo=self.user_repo,
                    transaction_repo=self.transaction_repo,
                    contest_repo=self.contest_repo,
                    problem_repo=self.problem_repo,
                    quiz_field_repo=quiz_field_repo,
                )
            )
        )

    async def get_remaining_number_of_attempts_for_selected_problems(
            self,
            selected_problem_ids: list[int],
            max_number_of_attempts: int = 3,
    ) -> dict[int, int]:
        # Правила DEFAULT подразумевают X попыток на решение задачи
        wrong_attempts_map: dict[int, int] = (
            await self.submission_repo.get_attempts_count_grouped_by_selected_problem_id(
                selected_problem_ids=selected_problem_ids,
                filter_by_verdict=[SubmissionVerdict.WRONG.value]
            )
        )
        attempts_by_selected_problem = {
            sp_id: max_number_of_attempts - wrong_attempts_map.get(sp_id, 0)
            for sp_id in selected_problem_ids
        }
        return attempts_by_selected_problem

    @log_calls
    async def get_contestant_selected_problems(
            self,
            user_id: int,
    ) -> ArraySelectedProblemInfoForContestant:

        contestant: Contestant = (
            await self.context_service.context.get_contestant_from_user(user_id=user_id)
        )

        rows: Sequence[Tuple[SelectedProblem, ProblemCard, Problem]] = (
            await self.selected_problem_repo.get_selected_problem_with_problem_card_and_problem_of_contestant_by_id(
                contestant_id=contestant.id,
            )
        )
        contest: Contest = (
            await self.context_service.context.get_contest_from_user(user_id=user_id)
        )

        attempts_by_selected_problem = {}
        if contest.rule_type == ContestRuleType.DEFAULT:
            attempts_by_selected_problem: dict[int, int] = (
                await self.get_remaining_number_of_attempts_for_selected_problems(
                    selected_problem_ids=[i[0].id for i in rows],  # Берем SelectedProblem.id из rows
                    max_number_of_attempts=MAX_NUMBER_OF_ATTEMPTS,
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
                    category_name=problem_card.category_name,
                    category_price=problem_card.category_price,
                    created_at=selected_problem.created_at,
                    attempts_remaining=attempts_by_selected_problem.get(selected_problem.id, None),
                ) for selected_problem, problem_card, problem in rows if
                selected_problem.status == SelectedProblemStatusType.ACTIVE
            ],
            rule_type=contest.rule_type,
            max_attempts_for_problem=MAX_NUMBER_OF_ATTEMPTS if contest.rule_type == ContestRuleType.DEFAULT else None,
        )
        return res

    @log_calls
    async def buy_selected_problem(
            self,
            user_id: int,
            problem_card_id: int,
    ) -> SelectedProblemId:
        user: User = (
            await self.context_service.context.get_user(user_id=user_id)
        )
        contestant: Contestant = (
            await self.context_service.context.get_contestant_from_user(user_id=user_id)
        )
        problem_card: ProblemCard | None = (
            await self.problem_card_repo.get_problem_card_by_id(problem_card_id=problem_card_id)
        )
        self.context_service.context.problem_card = problem_card

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
