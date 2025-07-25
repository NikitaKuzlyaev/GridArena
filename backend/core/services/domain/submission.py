from typing import Sequence

from backend.core.models import Contestant, ProblemCard, SelectedProblem, Problem
from backend.core.models.selected_problem import SelectedProblemStatusType
from backend.core.models.submission import SubmissionVerdict, Submission
from backend.core.repository.crud.contest import ContestCRUDRepository
from backend.core.repository.crud.contestant import ContestantCRUDRepository
from backend.core.repository.crud.problem import ProblemCRUDRepository
from backend.core.repository.crud.problem_card import ProblemCardCRUDRepository
from backend.core.repository.crud.quiz import QuizFieldCRUDRepository
from backend.core.repository.crud.selected_problem import SelectedProblemCRUDRepository
from backend.core.repository.crud.submission import SubmissionCRUDRepository
from backend.core.repository.crud.transaction import TransactionCRUDRepository
from backend.core.repository.crud.user import UserCRUDRepository
from backend.core.schemas.submission import SubmissionId
from backend.core.services.context.context import ContextService, ContextModel, RepositoryUnit
from backend.core.services.interfaces.submission import ISubmissionService
from backend.core.services.rules.submission_reward import calculate_max_submission_reward
from backend.core.utilities.exceptions.permission import PermissionDenied
from backend.core.utilities.formatters.string import make_string_clear
from backend.core.utilities.loggers.log_decorator import log_calls


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
                    quiz_field_repo=quiz_field_repo
                )
            ))

    def get_verdict(
            self,
            contestant_answer: str,
            problem_answer: str,
    ):
        clear_contestant_answer = make_string_clear(contestant_answer)
        clear_problem_answer = make_string_clear(problem_answer)
        return clear_contestant_answer == clear_problem_answer

    @log_calls
    async def check_submission(
            self,
            user_id: int,
            selected_problem_id: int,
            answer: str,
    ) -> SubmissionId:

        contestant: Contestant = await self.context_service.context.get_contestant_from_user(user_id=user_id)
        selected_problem: SelectedProblem = await self.context_service.context.get_selected_problem(
            selected_problem_id=selected_problem_id, )
        problem_card: ProblemCard = await self.context_service.context.get_problem_card_from_selected_problem()
        problem: Problem = await self.context_service.context.get_problem_from_problem_card(problem_card=problem_card)

        # Участник не может отправлять посылки не по своим купленным задачам
        if contestant.id != selected_problem.contestant_id:
            raise PermissionDenied("Участник не может отправлять посылки не по своим купленным задачам")

        is_answer_correct = self.get_verdict(
            contestant_answer=answer,
            problem_answer=problem.answer,
        )
        verdict = (SubmissionVerdict.ACCEPTED.value if is_answer_correct
                   else SubmissionVerdict.WRONG.value)
        possible_reward = 0
        if verdict == SubmissionVerdict.ACCEPTED.value:
            possible_reward: int = (
                await self.get_possible_reward(
                    selected_problem_id=selected_problem.id, ))

        next_status = await self.get_next_selected_problem_status(
            selected_problem_id=selected_problem.id,
            is_next_answer_correct=is_answer_correct,
        )

        submission: Submission = (
            await self.transaction_repo.create_submission(
                contestant_id=contestant.id,
                selected_problem_id=selected_problem_id,
                answer=answer,
                verdict=verdict,
                points_delta=possible_reward,
                selected_problem_change_status=next_status.value,
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

        selected_problem = await self.context_service.context.get_selected_problem(
            selected_problem_id=selected_problem_id, )
        problem_card = await self.context_service.context.get_problem_card_from_selected_problem(
            selected_problem_id=selected_problem.id, )
        quiz_field = await self.context_service.context.get_quiz_field_from_problem_card(
            problem_card=problem_card, )
        contest = await self.context_service.context.get_contest_from_quiz_field(
            quiz_field=quiz_field, )

        # Награда за решение доступна только если задача активна (доступна для решения)
        if selected_problem.status != SelectedProblemStatusType.ACTIVE:
            return 0

        submissions: Sequence[Submission] | None = (
            await self.submission_repo.get_submissions_of_selected_problem_by_id(
                selected_problem_id=selected_problem.id,
                filter_by_verdict=[SubmissionVerdict.WRONG.value], ))

        max_reward = calculate_max_submission_reward(
            number_of_tries_before=len(submissions),
            cost_of_problem_card=problem_card.category_price,
            contest_rule_type=contest.rule_type,
        )

        return max_reward

    async def get_next_selected_problem_status(
            self,
            selected_problem_id: int,
            is_next_answer_correct: bool,
    ) -> SelectedProblemStatusType:

        if is_next_answer_correct:
            return SelectedProblemStatusType.SOLVED

        selected_problem = await self.context_service.context.get_selected_problem(
            selected_problem_id=selected_problem_id, )

        submissions: Sequence[Submission] | None = (
            await self.submission_repo.get_submissions_of_selected_problem_by_id(
                selected_problem_id=selected_problem.id,
                filter_by_verdict=[SubmissionVerdict.WRONG.value], ))

        # Логика пока тут, лучше потом перенести
        # опять же: есть разные стратегии начисления баллов и правил игры
        # поэтому это костыль очень серьезный
        if len(submissions) < 2:
            return SelectedProblemStatusType.ACTIVE

        return SelectedProblemStatusType.FAILED
