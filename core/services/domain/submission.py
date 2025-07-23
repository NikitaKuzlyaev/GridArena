from typing import cast

from click import clear

from core.models import User, Contestant, ProblemCard, SelectedProblem, Contest, Problem
from core.repository.crud.contest import ContestCRUDRepository
from core.repository.crud.contestant import ContestantCRUDRepository
from core.repository.crud.problem import ProblemCRUDRepository
from core.repository.crud.problem_card import ProblemCardCRUDRepository
from core.repository.crud.selected_problem import SelectedProblemCRUDRepository
from core.repository.crud.submission import SubmissionCRUDRepository
from core.repository.crud.transaction import TransactionCRUDRepository
from core.repository.crud.user import UserCRUDRepository
from core.schemas.submission import SubmissionId

from core.services.interfaces.submission import ISubmissionService
from core.utilities.exceptions.database import EntityDoesNotExist, EntityAlreadyExists
from core.utilities.exceptions.permission import PermissionDenied
from core.utilities.loggers.log_decorator import log_calls


class SubmissionService(ISubmissionService):
    def __init__(
            self,
            submission_repo: SubmissionCRUDRepository,
            selected_problem_repo: SelectedProblemCRUDRepository,
            problem_card_repo: ProblemCardCRUDRepository,
            contestant_repo: ContestantCRUDRepository,
            user_repo: UserCRUDRepository,
            transaction_repo: TransactionCRUDRepository,
            contest_repo: ContestCRUDRepository,
            problem_repo: ProblemCRUDRepository,
    ):
        self.submission_repo = submission_repo
        self.selected_problem_repo = selected_problem_repo
        self.problem_card_repo = problem_card_repo
        self.contestant_repo = contestant_repo
        self.user_repo = user_repo
        self.transaction_repo = transaction_repo
        self.contest_repo = contest_repo
        self.problem_repo = problem_repo

    @log_calls
    async def check_submission(
            self,
            user_id: int,
            selected_problem_id: int,
            answer: str,
    ) -> SubmissionId:
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

        selected_problem: SelectedProblem | None = (
            await self.selected_problem_repo.get_selected_problem_by_id(
                selected_problem_id=selected_problem_id,
            )
        )
        if selected_problem:
            raise EntityAlreadyExists("selected problem already exists")

        if selected_problem.contestant_id != contestant.id:
            raise PermissionDenied("")

        problem_card: ProblemCard | None = (
            await self.problem_card_repo.get_problem_card_by_id(
                problem_card_id=cast(int, selected_problem.problem_card_id),
            )
        )
        if not problem_card:
            raise EntityDoesNotExist("problem card not found")

        problem: Problem | None = (
            await self.problem_repo.get_problem_by_id(
                problem_id=cast(int, problem_card.problem_id),
            )
        )
        if not problem:
            raise EntityDoesNotExist("problem not found")

        clear_answer = ''.join(answer.lower().strip().split())

        if problem.answer != clear_answer:
            res: SubmissionId = (
                await self.transaction_repo.create_submission(

                )
            )

        else:
            ...
            # res: SubmissionId = (
            #     await self.create_submission(
            #
            #     )
            # )

    # @log_calls
    # async def create_submission(
    #         self,
    #         user_id: int,
    #         selected_problem_id: int,
    #         answer: str,
    # ) -> SubmissionId: