from typing import Sequence

from pydantic import Field

from backend.core.schemas.base import BaseSchemaModel
from backend.core.schemas.problem_card import ProblemCardInfoForContestant, ProblemCardInfo


class QuizFieldId(BaseSchemaModel):
    quiz_field_id: int


class QuizFieldUpdateRequest(BaseSchemaModel):
    quiz_field_id: int
    number_of_rows: int = Field(
        ..., ge=1, le=8,
        description="Количество строк карточек",
    )
    number_of_columns: int = Field(
        ..., ge=1, le=8,
        description="Количество столбцов карточек",
    )


class QuizFieldCreateRequest(BaseSchemaModel):
    contest_id: int
    number_of_rows: int = Field(
        ..., ge=1, le=8,
        description="Количество строк карточек",
    )
    number_of_columns: int = Field(
        ..., ge=1, le=8,
        description="Количество столбцов карточек",
    )


class QuizFieldInfoForEditor(BaseSchemaModel):
    quiz_field_id: int
    number_of_rows: int
    number_of_columns: int
    problem_cards: Sequence[ProblemCardInfo]


class QuizFieldInfoForContestant(BaseSchemaModel):
    quiz_field_id: int
    number_of_rows: int
    number_of_columns: int
    problem_cards: Sequence[ProblemCardInfoForContestant]
