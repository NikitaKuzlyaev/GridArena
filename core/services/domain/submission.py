from dataclasses import dataclass
from typing import cast, Sequence

from core.models import User, Contestant, ProblemCard, SelectedProblem, Problem, QuizField, Contest
from core.models.selected_problem import SelectedProblemStatusType
from core.models.submission import SubmissionVerdict, Submission
from core.repository.crud.contest import ContestCRUDRepository
from core.repository.crud.contestant import ContestantCRUDRepository
from core.repository.crud.problem import ProblemCRUDRepository
from core.repository.crud.problem_card import ProblemCardCRUDRepository
from core.repository.crud.quiz import QuizFieldCRUDRepository
from core.repository.crud.selected_problem import SelectedProblemCRUDRepository
from core.repository.crud.submission import SubmissionCRUDRepository
from core.repository.crud.transaction import TransactionCRUDRepository
from core.repository.crud.user import UserCRUDRepository
from core.schemas.submission import SubmissionId
from core.services.context.context import ContextService
from core.services.interfaces.submission import ISubmissionService
from core.utilities.exceptions.database import EntityDoesNotExist, EntityAlreadyExists
from core.utilities.exceptions.permission import PermissionDenied
from core.utilities.loggers.log_decorator import log_calls


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
            quiz_field_repo: QuizFieldCRUDRepository,
    ):
        self.submission_repo = submission_repo
        self.selected_problem_repo = selected_problem_repo
        self.problem_card_repo = problem_card_repo
        self.contestant_repo = contestant_repo
        self.user_repo = user_repo
        self.transaction_repo = transaction_repo
        self.contest_repo = contest_repo
        self.problem_repo = problem_repo
        self.quiz_field_repo = quiz_field_repo
        self.repository_unit = RepositoryUnit(
            submission_repo=self.submission_repo,
            selected_problem_repo=self.selected_problem_repo,
            problem_card_repo=self.problem_card_repo,
            contestant_repo=self.contestant_repo,
            user_repo=self.user_repo,
            transaction_repo=self.transaction_repo,
            contest_repo=self.contest_repo,
            problem_repo=self.problem_repo,
            quiz_field_repo=quiz_field_repo
        )

    @staticmethod
    def make_string_clear(
            string: str,
    ) -> str:
        return ''.join(string.lower().strip().split())

    def get_verdict(
            self,
            contestant_answer: str,
            problem_answer: str,
    ):
        clear_contestant_answer = self.make_string_clear(contestant_answer)
        clear_problem_answer = self.make_string_clear(problem_answer)
        return clear_contestant_answer == clear_problem_answer

    @log_calls
    async def check_submission(
            self,
            user_id: int,
            selected_problem_id: int,
            answer: str,
    ) -> SubmissionId:
        ctx = ContextService()

        user, contestant, selected_problem, problem_card, problem = (
            await ctx.get_selected_problem_context(
                repository_unit=self.repository_unit,
                selected_problem_id=selected_problem_id,
            )
        ).unpack()

        # Участник не может отправлять посылки не по своим купленным задачам
        if contestant.id != selected_problem.contestant_id:
            raise PermissionDenied()

        is_answer_correct = self.get_verdict(
            contestant_answer=answer,
            problem_answer=problem.answer,
        )
        verdict = SubmissionVerdict.ACCEPTED.value if is_answer_correct else SubmissionVerdict.REJECTED.value

        possible_reward: int = (
            await self.get_possible_reward(
                selected_problem_id=selected_problem.id,
            )
        )

        submission: Submission = (
            await self.transaction_repo.create_submission(
                contestant_id=contestant.id,
                selected_problem_id=selected_problem_id,
                answer=answer,
                verdict=verdict,
                points_delta=possible_reward,
            )
        )

        res = SubmissionId(
            submission_id=submission.id,
        )

        return res

    async def get_possible_reward(
            self,
            selected_problem_id: int,
    ) -> int:
        selected_problem: SelectedProblem | None = (
            await self.selected_problem_repo.get_selected_problem_by_id(
                selected_problem_id=selected_problem_id, ))
        if not selected_problem:
            raise EntityDoesNotExist("")

        # Награда за решение доступна только если задача активна (доступна для решения)
        if selected_problem.status != SelectedProblemStatusType.ACTIVE:
            return 0

        problem_card: ProblemCard = (
            await self.problem_card_repo.get_problem_card_by_id(
                problem_card_id=selected_problem.problem_card_id, ))
        quiz_field: QuizField = (
            await self.quiz_field_repo.get_quiz_field_by_id(
                quiz_field_id=problem_card.quiz_field_id, ))
        contest: Contest = (
            await self.contest_repo.get_contest_by_id(
                contest_id=quiz_field.contest_id, ))

        submissions: Sequence[Submission] | None = (
            await self.submission_repo.get_submissions_of_selected_problem_by_id(
                selected_problem_id=selected_problem.id,
                filter_by_verdict=[SubmissionVerdict.WRONG.value],
            )
        )



        return 0
