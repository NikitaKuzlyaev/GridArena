from typing import Sequence

from backend.core.models import (
    Contestant,
    ProblemCard,
    SelectedProblem,
    Problem,
    QuizField,
    Contest,
)
from backend.core.models.selected_problem import SelectedProblemStatusType
from backend.core.models.submission import (
    SubmissionVerdict,
    Submission,
)
from backend.core.repository.crud.uow import UnitOfWork
from backend.core.schemas.submission import SubmissionId
from backend.core.services.interfaces.submission import ISubmissionService
from backend.core.services.rules.submission_reward import calculate_max_submission_reward
from backend.core.utilities.exceptions.permission import PermissionDenied
from backend.core.utilities.formatters.string import make_string_clear
from backend.core.utilities.loggers.log_decorator import log_calls


class SubmissionService(ISubmissionService):
    def __init__(
            self,
            uow: UnitOfWork,
    ):
        self.uow = uow

    def _get_verdict(
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
        async with self.uow:
            # Проверка прав не требуется. Все описано в логике ниже.
            # Пользователь не может получить чужую информацию в принципе, так как жестко привязан своим domain_number

            contestant: Contestant = await self.uow.contestant_repo.get_contestant_by_user_id(user_id=user_id, )
            selected_problem: SelectedProblem = (
                await self.uow.selected_problem_repo.get_selected_problem_by_id(
                    selected_problem_id=selected_problem_id, )
            )
            problem_card: ProblemCard = (
                await self.uow.problem_card_repo.get_problem_card_by_id(
                    problem_card_id=selected_problem.problem_card_id, )
            )
            problem: Problem = await self.uow.problem_repo.get_problem_by_id(problem_id=problem_card.problem_id, )

            # Участник не может отправлять посылки не по своим купленным задачам
            if contestant.id != selected_problem.contestant_id:
                raise PermissionDenied("Участник не может отправлять посылки не по своим купленным задачам")

            is_answer_correct = self._get_verdict(
                contestant_answer=answer,
                problem_answer=problem.answer,
            )

            verdict = SubmissionVerdict.ACCEPTED.value if is_answer_correct else SubmissionVerdict.WRONG.value

            possible_reward = 0

            if verdict == SubmissionVerdict.ACCEPTED.value:
                possible_reward: int = (
                    await self._get_possible_reward(
                        selected_problem_id=selected_problem.id, )
                )

            next_status = await self._get_next_selected_problem_status(
                selected_problem_id=selected_problem.id,
                is_next_answer_correct=is_answer_correct,
            )

            submission: Submission = (
                await self.uow.transaction_repo.create_submission(
                    contestant_id=contestant.id,
                    selected_problem_id=selected_problem_id,
                    answer=answer,
                    verdict=verdict,
                    points_delta=possible_reward,
                    selected_problem_change_status=next_status.value, )
            )
            res = SubmissionId(
                submission_id=submission.id,
            )
            return res

    async def _get_possible_reward(
            self,
            selected_problem_id: int,
    ) -> int:
        async with self.uow:
            selected_problem: SelectedProblem = (
                await self.uow.selected_problem_repo.get_selected_problem_by_id(
                    selected_problem_id=selected_problem_id, )
            )
            problem_card: ProblemCard = (
                await self.uow.problem_card_repo.get_problem_card_by_id(
                    problem_card_id=selected_problem.problem_card_id, )
            )
            quiz_field: QuizField = (
                await self.uow.quiz_field_repo.get_quiz_field_by_id(quiz_field_id=problem_card.quiz_field_id, )
            )
            contest: Contest = (
                await self.uow.contest_repo.get_contest_by_id(contest_id=quiz_field.contest_id, )
            )

            # Награда за решение доступна только если задача активна (доступна для решения)
            if selected_problem.status != SelectedProblemStatusType.ACTIVE:
                return 0

            submissions: Sequence[Submission] | None = (
                await self.uow.submission_repo.get_submissions_of_selected_problem_by_id(
                    selected_problem_id=selected_problem.id,
                    filter_by_verdict=[
                        SubmissionVerdict.WRONG.value,
                    ],
                )
            )
            max_reward = calculate_max_submission_reward(
                number_of_tries_before=len(submissions),
                cost_of_problem_card=problem_card.category_price,
                contest_rule_type=contest.rule_type,
            )
            return max_reward

    async def _get_next_selected_problem_status(
            self,
            selected_problem_id: int,
            is_next_answer_correct: bool,
    ) -> SelectedProblemStatusType:
        async with self.uow:
            if is_next_answer_correct:
                return SelectedProblemStatusType.SOLVED

            selected_problem: SelectedProblem = (
                await self.uow.selected_problem_repo.get_selected_problem_by_id(selected_problem_id=selected_problem_id)
            )
            submissions: Sequence[Submission] | None = (
                await self.uow.submission_repo.get_submissions_of_selected_problem_by_id(
                    selected_problem_id=selected_problem.id,
                    filter_by_verdict=[
                        SubmissionVerdict.WRONG.value,
                    ],
                )
            )
            # Логика пока тут, лучше потом перенести
            # опять же: есть разные стратегии начисления баллов и правил игры
            # поэтому это костыль очень серьезный
            if len(submissions) < 2:
                return SelectedProblemStatusType.ACTIVE

            return SelectedProblemStatusType.FAILED
