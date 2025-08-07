from typing import (
    Sequence,
    Tuple,
    Optional,
)

from sqlalchemy import Row

from backend.core.models import (
    QuizField,
    ProblemCard,
    Problem,
    SelectedProblem,
)
from backend.core.models.selected_problem import SelectedProblemStatusType
from backend.core.repository.crud.uow import UnitOfWork
from backend.core.schemas.problem import ProblemId
from backend.core.schemas.problem_card import (
    ProblemCardInfo,
    ProblemCardInfoForContestant,
    ProblemCardStatus,
)
from backend.core.schemas.quiz_field import (
    QuizFieldId,
    QuizFieldInfoForEditor,
    QuizFieldInfoForContestant, QuizFieldUpdateRequest,
)
from backend.core.services.access_policies.quiz_field import QuizFieldAccessPolicy
from backend.core.services.interfaces.quiz_field import IQuizFieldService
from backend.core.utilities.loggers.log_decorator import log_calls

MAPPING_SP2PC = {
    SelectedProblemStatusType.ACTIVE: ProblemCardStatus.SOLVING,
    SelectedProblemStatusType.REJECTED: ProblemCardStatus.REJECTED,
    SelectedProblemStatusType.SOLVED: ProblemCardStatus.SOLVED,
    SelectedProblemStatusType.FAILED: ProblemCardStatus.FAILED,
}


class QuizFieldService(IQuizFieldService):
    def __init__(
            self,
            uow: UnitOfWork,
            access_policy: Optional[QuizFieldAccessPolicy] = None,
    ):
        self.uow = uow
        self.access_policy: QuizFieldAccessPolicy = access_policy or QuizFieldAccessPolicy()

    @log_calls
    async def quiz_field_info_for_contestant(
            self,
            user_id,
    ) -> QuizFieldInfoForContestant:
        async with self.uow:
            # Проверка прав не требуется. Все описано в логике ниже.
            # Пользователь не может получить чужую информацию в принципе, так как жестко привязан своим domain_number

            user, contestant, contest, quiz_field = (
                await self.uow.domain_repo.get_contestant_full_context(user_id=user_id, )
            )
            problem_cards_with_problem: Sequence[Row[Tuple[ProblemCard, Problem]]] = (
                await self.uow.problem_card_repo.get_tuple_problem_cards_with_problem_by_quiz_field_id(
                    quiz_field_id=quiz_field.id, )
            )
            selected_problems: Sequence[SelectedProblem] = (
                await self.uow.selected_problem_repo.get_selected_problem_of_contestant_by_id(
                    contestant_id=contestant.id, )
            )

            selected_problems_statuses = {sp.problem_card_id: sp.status for sp in selected_problems}
            active_count = sum(
                status == SelectedProblemStatusType.ACTIVE for status in selected_problems_statuses.values())

            problem_cards = []

            for problem_card, problem in problem_cards_with_problem:
                status = MAPPING_SP2PC.get(selected_problems_statuses.get(problem_card.id), ProblemCardStatus.CLOSED)

                if selected_problems_statuses.get(problem_card.id) is None or status == ProblemCardStatus.CLOSED:
                    can_buy = (
                            active_count < contest.number_of_slots_for_problems
                            and problem_card.category_price <= contestant.points
                    )
                    if can_buy:
                        status = ProblemCardStatus.OPEN
                else:
                    can_buy = False

                problem_cards.append(
                    self._map_problem_card_info_for_contestant(problem_card, problem, status, can_buy, ))

            res = self._map_quiz_field_info_for_contestant(quiz_field, problem_cards, )
            return res

    @log_calls
    async def quiz_field_info_for_editor(
            self,
            user_id,
            contest_id,
    ) -> QuizFieldInfoForEditor:
        async with self.uow:
            await self.access_policy.can_user_manage_contest(
                uow=self.uow, user_id=user_id, contest_id=contest_id, raise_if_none=True, )

            quiz_field: QuizField = await self.uow.quiz_field_repo.get_quiz_field_by_contest_id(
                contest_id=contest_id, )

            problem_cards_with_problem: Sequence[Row[Tuple[ProblemCard, Problem]]] = (
                await self.uow.problem_card_repo.get_tuple_problem_cards_with_problem_by_quiz_field_id(
                    quiz_field_id=quiz_field.id, )
            )

            res = self._map_quiz_field_info_editor(quiz_field, problem_cards_with_problem, )
            return res

    @log_calls
    async def update_quiz_field(
            self,
            user_id: int,
            data: QuizFieldUpdateRequest,
    ) -> QuizFieldId:
        async with self.uow:
            await self.access_policy.can_user_edit_quiz_field(
                uow=self.uow, user_id=user_id, quiz_field_id=data.quiz_field_id, raise_if_none=True, )

            quiz_field: QuizField = await self.uow.quiz_field_repo.update_quiz_field(**data.model_dump(), )

            res = QuizFieldId(quiz_field_id=quiz_field.id, )
            return res

    @staticmethod
    def _map_quiz_field_info_editor(
            quiz_field: QuizField,
            problem_cards_with_problem: Sequence[Row[Tuple[ProblemCard, Problem]]],  # What the hell?
    ) -> QuizFieldInfoForEditor:
        res = QuizFieldInfoForEditor(
            quiz_field_id=quiz_field.id,
            number_of_rows=quiz_field.number_of_rows,
            number_of_columns=quiz_field.number_of_columns,
            problem_cards=[
                ProblemCardInfo(
                    problem_card_id=problem_card.id,
                    problem=ProblemId(
                        problem_id=problem.id,
                    ),
                    row=problem_card.row,
                    column=problem_card.column,
                    category_price=problem_card.category_price,
                    category_name=problem_card.category_name,
                ) for problem_card, problem in problem_cards_with_problem
            ],
        )
        return res

    @staticmethod
    def _map_problem_card_info_for_contestant(
            problem_card: ProblemCard,
            problem: Problem,
            status: ProblemCardStatus,
            can_buy: bool,
    ) -> ProblemCardInfoForContestant:
        res = ProblemCardInfoForContestant(
            problem_card_id=problem_card.id,
            problem=ProblemId(problem_id=problem.id),
            status=status,
            is_open_for_buy=can_buy,
            row=problem_card.row,
            column=problem_card.column,
            category_price=problem_card.category_price,
            category_name=problem_card.category_name,
        )
        return res

    @staticmethod
    def _map_quiz_field_info_for_contestant(
            quiz_field: QuizField,
            problem_cards: Sequence[ProblemCardInfoForContestant],
    ) -> QuizFieldInfoForContestant:
        res = QuizFieldInfoForContestant(
            quiz_field_id=quiz_field.id,
            number_of_rows=quiz_field.number_of_rows,
            number_of_columns=quiz_field.number_of_columns,
            problem_cards=problem_cards,
        )
        return res
