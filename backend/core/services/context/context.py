from dataclasses import dataclass

from backend.core.models import QuizField, User, Contestant, SelectedProblem, ProblemCard, Problem, Contest
from backend.core.repository.crud.contest import ContestCRUDRepository
from backend.core.repository.crud.contestant import ContestantCRUDRepository
from backend.core.repository.crud.problem import ProblemCRUDRepository
from backend.core.repository.crud.problem_card import ProblemCardCRUDRepository
from backend.core.repository.crud.quiz import QuizFieldCRUDRepository
from backend.core.repository.crud.selected_problem import SelectedProblemCRUDRepository
from backend.core.repository.crud.submission import SubmissionCRUDRepository
from backend.core.repository.crud.transaction import TransactionCRUDRepository
from backend.core.repository.crud.user import UserCRUDRepository
from backend.core.services.interfaces.context import IContextService
from backend.core.utilities.exceptions.data_structures import NotEnoughParameters
from backend.core.utilities.exceptions.database import EntityDoesNotExist
from backend.core.utilities.loggers.log_decorator import log_calls


@dataclass
class RepositoryUnit:
    submission_repo: SubmissionCRUDRepository
    selected_problem_repo: SelectedProblemCRUDRepository
    problem_card_repo: ProblemCardCRUDRepository
    contestant_repo: ContestantCRUDRepository
    user_repo: UserCRUDRepository
    transaction_repo: TransactionCRUDRepository
    contest_repo: ContestCRUDRepository
    problem_repo: ProblemCRUDRepository
    quiz_field_repo: QuizFieldCRUDRepository


@dataclass
class ContextModel:
    repository_unit: RepositoryUnit
    user: User | None = None
    contestant: Contestant | None = None
    selected_problem: SelectedProblem | None = None
    problem_card: ProblemCard | None = None
    problem: Problem | None = None
    quiz_field: QuizField | None = None
    contest: Contest | None = None

    @log_calls
    async def get_user(self, **kwargs) -> User | None:
        if self.user:
            return self.user

        user_id: int | None = kwargs.get("user_id")
        if not user_id:
            raise NotEnoughParameters("user_id")

        user: User | None = (
            await self.repository_unit.user_repo.get_user_by_id(
                user_id=user_id,
            )
        )
        if not user:
            raise EntityDoesNotExist("user not found")

        self.user = user
        return user

    @log_calls
    async def get_contestant_from_user(
            self,
            **kwargs,
    ) -> Contestant:
        if self.contestant:
            return self.contestant

        user: User | None = self.user
        if not user:

            user_id: int | None = kwargs.get("user_id")
            if user_id: user: User | None = (
                await self.repository_unit.user_repo.get_user_by_id(
                    user_id=user_id,
                )
            )
            if not user:
                raise EntityDoesNotExist("user not found")

            self.user = user

        self.contestant = (
            await self.repository_unit.contestant_repo.get_contestant_by_user_id(
                user_id=user.id,
            )
        )
        return self.contestant

    @log_calls
    async def get_problem_from_problem_card(
            self,
            **kwargs,
    ) -> Problem:
        if self.problem:
            return self.problem

        problem_card: ProblemCard | None = self.problem_card
        if not problem_card:

            problem_card_id: int | None = kwargs.get("problem_card_id")
            if problem_card_id:
                problem_card: ProblemCard | None = (
                    await self.repository_unit.problem_card_repo.get_problem_card_by_id(
                        problem_card_id=problem_card_id,
                    )
                )

            if not problem_card:
                raise EntityDoesNotExist("problem_card not found")

        self.problem = (
            await self.repository_unit.problem_repo.get_problem_by_id(
                problem_id=problem_card.problem_id,
            )
        )
        return self.problem

    @log_calls
    async def get_problem_card_from_selected_problem(
            self,
            **kwargs,
    ) -> ProblemCard:
        if self.problem_card:
            return self.problem_card

        selected_problem: SelectedProblem | None = self.selected_problem
        if not selected_problem:

            selected_problem_id: int | None = kwargs.get("selected_problem_id")
            if selected_problem_id:
                selected_problem: SelectedProblem | None = (
                    await self.repository_unit.selected_problem_repo.get_selected_problem_by_id(
                        selected_problem_id=selected_problem_id,
                    )
                )

            if not selected_problem:
                raise EntityDoesNotExist("selected_problem not found")

        self.problem_card = (
            await self.repository_unit.problem_card_repo.get_problem_card_by_id(
                problem_card_id=selected_problem.problem_card_id,
            )
        )
        return self.problem_card

    @log_calls
    async def get_quiz_field_from_problem_card(
            self,
            **kwargs,
    ) -> QuizField:
        if self.quiz_field:
            return self.quiz_field

        problem_card: ProblemCard | None = (
            await self.get_problem_card_from_selected_problem(**kwargs)
        )
        if not problem_card:

            problem_card_id: int | None = kwargs.get("problem_card_id")
            if problem_card_id:
                problem_card: ProblemCard | None = (
                    await self.repository_unit.problem_card_repo.get_problem_card_by_id(
                        problem_card_id=problem_card_id,
                    )
                )

            if not problem_card:
                raise EntityDoesNotExist("problem_card not found")

        self.quiz_field = (
            await self.repository_unit.quiz_field_repo.get_quiz_field_by_id(
                quiz_field_id=problem_card.quiz_field_id,
            )
        )
        return self.quiz_field

    @log_calls
    async def get_contest_from_quiz_field(
            self,
            **kwargs,
    ) -> Contest:
        if self.contest:
            return self.contest

        quiz_field: QuizField | None = (
            await self.get_quiz_field_from_problem_card(**kwargs)
        )
        if not quiz_field:

            quiz_field_id: int | None = kwargs.get("quiz_field_id")
            if quiz_field_id:
                quiz_field: QuizField | None = (
                    await self.repository_unit.quiz_field_repo.get_quiz_field_by_id(
                        quiz_field_id=quiz_field_id,
                    )
                )

            if not quiz_field:
                raise EntityDoesNotExist("quiz_field not found")

        self.contest = (
            await self.repository_unit.contest_repo.get_contest_by_id(
                contest_id=quiz_field.contest_id,
            )
        )
        return self.contest

    @log_calls
    async def get_contest_from_user(
            self,
            **kwargs,
    ) -> Contest:
        if self.contest:
            return self.contest

        user: User | None = (
            await self.get_user(**kwargs)
        )
        if not user:

            user_id: int | None = kwargs.get("user_id")
            if user_id:
                user: User | None = (
                    await self.repository_unit.user_repo.get_user_by_id(
                        user_id=user_id,
                    )
                )

            if not user:
                raise EntityDoesNotExist("user not found")

        self.contest = (
            await self.repository_unit.contest_repo.get_contest_by_id(
                contest_id=user.domain_number,
            )
        )
        return self.contest

    @log_calls
    async def get_selected_problem(
            self,
            **kwargs,
    ) -> SelectedProblem:
        if self.selected_problem:
            return self.selected_problem

        selected_problem_id: int | None = kwargs.get("selected_problem_id")
        selected_problem = None

        if selected_problem_id:
            selected_problem: SelectedProblem | None = (
                await self.repository_unit.selected_problem_repo.get_selected_problem_by_id(
                    selected_problem_id=selected_problem_id,
                )
            )

        if not selected_problem:
            raise EntityDoesNotExist("selected_problem not found")

        self.selected_problem = selected_problem
        return self.selected_problem


class ContextService(IContextService):

    def __init__(self, context: ContextModel):
        self.context = context
