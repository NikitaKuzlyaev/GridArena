from typing import (
    Sequence,
    Type,
)

from pydantic import (
    Field,
    ValidationError,
)

from backend.core.models import (
    Contestant,
    ProblemCard,
    SelectedProblem,
    Problem,
    QuizField,
    Contest,
)
from backend.core.models.contestant_log import ContestantLogLevelType
from backend.core.models.selected_problem import SelectedProblemStatusType
from backend.core.models.submission import (
    SubmissionVerdict,
    Submission,
)
from backend.core.repository.crud.uow import UnitOfWork
from backend.core.schemas.base import BaseSchemaModel
from backend.core.schemas.contestant_log import LogMessage
from backend.core.schemas.submission import SubmissionId
from backend.core.services.interfaces.submission import ISubmissionService
from backend.core.services.rules.submission_reward import calculate_max_submission_reward
from backend.core.utilities.exceptions.permission import PermissionDenied
from backend.core.utilities.formatters.string import make_string_clear
from backend.core.utilities.loggers.log_decorator import log_calls


class AnswerValidatorModel(BaseSchemaModel):
    """
    Модель для валидации ответа пользователя.

    Валидация не означает проверку ответа на правильность - выполняется проверка соответствия записи ответа.
    Например: ответ не может быть пустым или слишком длинным.
    """
    # Текущая валидация - только по соответствию длины
    answer: str = Field(..., min_length=1, max_length=32)


class SubmissionService(ISubmissionService):
    def __init__(
            self,
            uow: UnitOfWork,
    ):
        self.uow = uow

    @staticmethod
    def _are_strings_equal(
            contestant_answer: str,
            problem_answer: str,
    ):
        clear_contestant_answer = make_string_clear(contestant_answer)
        clear_problem_answer = make_string_clear(problem_answer)
        return clear_contestant_answer == clear_problem_answer

    @staticmethod
    def _is_answer_valid_by_model(
            answer: str,
            validate_model: Type[BaseSchemaModel],
    ) -> bool:
        """
        Функция для проверки ответа участника на соответствие переданной модели.
        """
        try:
            # Попытка создать модель. Любые исключения несоответствия в таком случае инициируются только Pydantic.
            validate_model(answer=answer)
            return True
        except ValidationError:
            return False

    # todo: реальная проверка ответа не должна блокировать основной поток -> проверять в воркере
    #   Создавать только инстанс посылки и задачу в воркер. Пользователю отдавать статус "на проверке"
    #   Это имеет смысл для расширяемости в будущем, даже если сейчас проверка относительно быстрая
    #   (в планах сделать автогенерацию тестов и проверку ответов в свободной форме с помощью ллм)
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

            # Валидация ответа (не принимать ответы, которые не соответствуют модели)
            # В случае, если ответ был передан без валидации на уровне эндпоинта, или попал сюда любым иным способом
            is_answer_valid_by_model = self._is_answer_valid_by_model(answer, validate_model=AnswerValidatorModel)
            if not is_answer_valid_by_model:
                raise ValueError("Contestant answer is invalid")

            # Не принимать ответ, если он уже был.
            # Что делать, если к задаче ответ был неверный, а потом поменялся, и участник его уже отправлял?
            # Что делать?
            # todo: добавить систему перепроверки? разрешить отправку повторного ответа? возвращать все submission?
            # Пока не предпринимаю никаких действий. Такой же ответ можно отправить повторно.

            is_answer_correct = self._are_strings_equal(
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

            if next_status == SelectedProblemStatusType.ACTIVE or next_status == SelectedProblemStatusType.FAILED:
                # Пишем лог о том, что ответ неверный
                await self.uow.contestant_log_repo.create_log(
                    contestant_id=contestant.id,
                    log_level=ContestantLogLevelType.INFO,
                    content=LogMessage.wrong_answer(),
                )
            if next_status == SelectedProblemStatusType.FAILED:
                # Пишем лог о том, что задача "сгорела"
                ...
            if next_status == SelectedProblemStatusType.SOLVED:
                # Пишем лог о том, что ответ верный
                await self.uow.contestant_log_repo.create_log(
                    contestant_id=contestant.id,
                    log_level=ContestantLogLevelType.INFO,
                    content=LogMessage.correct_answer(),
                )
                await self.uow.contestant_log_repo.create_log(
                    contestant_id=contestant.id,
                    log_level=ContestantLogLevelType.INFO,
                    content=LogMessage.balance_increase(points=possible_reward),
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
        # async with self.uow: -> Вызывается из check_submission(...)
        # Осторожно!
        # Этот метод должен вызываться исключительно из кода внутри async with self.uow
        # (внутри контекстного менеджера, управляющего сессией к базе данных)

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
        # async with self.uow: -> Вызывается из check_submission(...)
        # Осторожно!
        # Этот метод должен вызываться исключительно из кода внутри async with self.uow
        # (внутри контекстного менеджера, управляющего сессией к базе данных)

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
