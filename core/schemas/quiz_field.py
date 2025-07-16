from core.models import ProblemCard
from core.schemas.base import BaseSchemaModel
from datetime import datetime
from typing import Optional, Sequence

from pydantic import Field, validator, root_validator, model_validator

from core.schemas.problem_card import ProblemCardInfoForEditor, ProblemCardInfoForContestant, ProblemCardInfo


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
