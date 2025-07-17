from typing import Sequence, Tuple

from sqlalchemy import Row

from core.models import QuizField, ProblemCard, Problem
from core.repository.crud.problem_card import ProblemCardCRUDRepository
from core.repository.crud.quiz import QuizFieldCRUDRepository
from core.schemas.problem import ProblemId
from core.schemas.problem_card import ProblemCardInfo
from core.schemas.quiz_field import QuizFieldId, QuizFieldInfoForEditor
from core.services.interfaces.quiz import IQuizFieldService
from core.utilities.exceptions.database import EntityDoesNotExist
from core.utilities.loggers.log_decorator import log_calls


class QuizFieldService(IQuizFieldService):
    def __init__(
            self,
            quiz_field_repo: QuizFieldCRUDRepository,
            problem_card_repo: ProblemCardCRUDRepository,
    ):
        self.quiz_field_repo = quiz_field_repo
        self.problem_card_repo = problem_card_repo

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

        problem_cards: Sequence[ProblemCard] = (
            await self.problem_card_repo.get_problem_cards_by_quiz_field_id(
                quiz_field_id=quiz_field.id,
            )
        )

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
        res = QuizFieldId(quiz_field_id=quiz_field.id)

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

        res = QuizFieldId(quiz_field_id=quiz_field.id)
        return res
