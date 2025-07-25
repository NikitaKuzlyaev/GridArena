from typing import Sequence, Tuple

from sqlalchemy import Row

from backend.core.models import (
    QuizField, ProblemCard, Problem, User, Contestant, SelectedProblem, Contest)
from backend.core.models.selected_problem import SelectedProblemStatusType
from backend.core.repository.crud.contest import ContestCRUDRepository
from backend.core.repository.crud.contestant import ContestantCRUDRepository
from backend.core.repository.crud.problem_card import ProblemCardCRUDRepository
from backend.core.repository.crud.quiz import QuizFieldCRUDRepository
from backend.core.repository.crud.selected_problem import SelectedProblemCRUDRepository
from backend.core.repository.crud.user import UserCRUDRepository
from backend.core.schemas.problem import ProblemId
from backend.core.schemas.problem_card import ProblemCardInfo, ProblemCardInfoForContestant, ProblemCardStatus
from backend.core.schemas.quiz_field import QuizFieldId, QuizFieldInfoForEditor, QuizFieldInfoForContestant
from backend.core.services.interfaces.quiz import IQuizFieldService
from backend.core.utilities.exceptions.data_structures import UndefinedMapping
from backend.core.utilities.exceptions.database import EntityDoesNotExist
from backend.core.utilities.loggers.log_decorator import log_calls


class QuizFieldService(IQuizFieldService):
    def __init__(
            self,
            quiz_field_repo: QuizFieldCRUDRepository,
            problem_card_repo: ProblemCardCRUDRepository,
            contestant_repo: ContestantCRUDRepository,
            user_repo: UserCRUDRepository,
            selected_problem_repo: SelectedProblemCRUDRepository,
            contest_repo: ContestCRUDRepository,
    ):
        self.quiz_field_repo = quiz_field_repo
        self.problem_card_repo = problem_card_repo
        self.contestant_repo = contestant_repo
        self.user_repo = user_repo
        self.selected_problem_repo = selected_problem_repo
        self.contest_repo = contest_repo

    @log_calls
    async def quiz_field_info_for_contestant(
            self,
            user_id,
    ) -> QuizFieldInfoForContestant:
        user: User = (
            await self.user_repo.get_user_by_id(
                user_id=user_id,
            )
        )
        contest_id = user.domain_number

        contest: Contest = (
            await self.contest_repo.get_contest_by_id(
                contest_id=contest_id,
            )
        )
        quiz_field: QuizField = (
            await self.quiz_field_repo.get_quiz_field_by_contest_id(
                contest_id=contest_id,
            )
        )
        problem_cards_with_problem: Sequence[Row[Tuple[ProblemCard, Problem]]] = (
            await self.problem_card_repo.get_tuple_problem_cards_with_problem_by_quiz_field_id(
                quiz_field_id=quiz_field.id,
            )
        )
        contestant: Contestant = (
            await self.contestant_repo.get_contestant_by_user_id(
                user_id=user_id,
            )
        )
        selected_problems: Sequence[SelectedProblem] = (
            await self.selected_problem_repo.get_selected_problem_of_contestant_by_id(
                contestant_id=contestant.id,
            )
        )
        selected_problems_statuses = {
            sp.problem_card_id: sp.status for sp in selected_problems
        }

        problem_cards = []

        number_of_active_selected_problems = sum(
            sp.status == SelectedProblemStatusType.ACTIVE for sp in selected_problems
        )

        for problem_card, problem in problem_cards_with_problem:
            status = ProblemCardStatus.CLOSED

            if problem_card.id in selected_problems_statuses:
                st = selected_problems_statuses[problem_card.id]

                if st == SelectedProblemStatusType.ACTIVE:
                    status = ProblemCardStatus.SOLVING
                elif st == SelectedProblemStatusType.REJECTED:
                    status = ProblemCardStatus.REJECTED
                elif st == SelectedProblemStatusType.SOLVED:
                    status = ProblemCardStatus.SOLVED
                elif st == SelectedProblemStatusType.FAILED:
                    status = ProblemCardStatus.FAILED
                else:
                    raise UndefinedMapping("Не определен маппинг SelectedProblemStatusType -> ProblemCardStatus")

            else:
                pass

            is_open_for_buy: bool = all(
                [
                    number_of_active_selected_problems < contest.number_of_slots_for_problems,
                    status == ProblemCardStatus.CLOSED,
                    problem_card.category_price <= contestant.points,
                ]
            )

            if status == ProblemCardStatus.CLOSED and is_open_for_buy:
                status = ProblemCardStatus.OPEN

            upd = ProblemCardInfoForContestant(
                problem_card_id=problem_card.id,
                problem=ProblemId(
                    problem_id=problem.id,
                ),
                status=status,
                is_open_for_buy=is_open_for_buy,
                row=problem_card.row,
                column=problem_card.column,
                category_price=problem_card.category_price,
                category_name=problem_card.category_name,
            )
            problem_cards.append(upd)

        res = QuizFieldInfoForContestant(
            quiz_field_id=quiz_field.id,
            number_of_rows=quiz_field.number_of_rows,
            number_of_columns=quiz_field.number_of_columns,
            problem_cards=problem_cards,
        )
        return res

    @log_calls
    async def quiz_field_info_for_editor(
            self,
            user_id,
            contest_id,
    ) -> QuizFieldInfoForEditor:

        quiz_field: QuizField | None = (
            await self.quiz_field_repo.get_quiz_field_by_contest_id(
                contest_id=contest_id,
            )
        )
        if not quiz_field:
            raise EntityDoesNotExist("quiz_field with such contest_id not found")

        problem_cards_with_problem: Sequence[Row[Tuple[ProblemCard, Problem]]] = (
            await self.problem_card_repo.get_tuple_problem_cards_with_problem_by_quiz_field_id(
                quiz_field_id=quiz_field.id,
            )
        )
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

    @log_calls
    async def create_quiz_field(
            self,
            contest_id: int,
            number_of_rows: int,
            number_of_columns: int,
    ) -> QuizFieldId:
        quiz_field: QuizField = (
            await self.quiz_field_repo.create_quiz_field(
                contest_id=contest_id,
                number_of_rows=number_of_rows,
                number_of_columns=number_of_columns,
            )
        )
        res = QuizFieldId(
            quiz_field_id=quiz_field.id,
        )
        return res

    @log_calls
    async def update_quiz_field(
            self,
            quiz_field_id: int,
            number_of_rows: int,
            number_of_columns: int,
    ) -> QuizFieldId:
        quiz_field: QuizField | None = (
            await self.quiz_field_repo.update_quiz_field(
                quiz_field_id=quiz_field_id,
                number_of_rows=number_of_rows,
                number_of_columns=number_of_columns,
            )
        )
        if not quiz_field:
            raise EntityDoesNotExist("quiz_field with such quiz_field_id not found")

        res = QuizFieldId(
            quiz_field_id=quiz_field.id,
        )
        return res
