from enum import Enum

from pydantic import Field

from backend.core.schemas.base import BaseSchemaModel
from backend.core.schemas.problem import (
    ProblemInfoForEditor,
    ProblemId,
)


class ProblemCardId(BaseSchemaModel):
    problem_card_id: int


class ProblemCardUpdateRequest(BaseSchemaModel):
    problem_card_id: int
    category_name: str = Field(..., max_length=32)
    category_price: int = Field(..., ge=0, le=10000)


class ProblemCardWithProblemUpdateRequest(BaseSchemaModel):
    problem_card_id: int
    problem_id: int
    category_name: str = Field(..., max_length=32)
    category_price: int = Field(..., ge=0, le=10000)
    statement: str = Field(..., max_length=2048)
    answer: str = Field(..., max_length=32)


class ProblemCardWithProblemCreateRequest(BaseSchemaModel):
    quiz_field_id: int
    row: int
    column: int
    category_name: str = Field(..., max_length=32)
    category_price: int = Field(..., ge=0, le=10000)
    statement: str = Field(..., max_length=2048)
    answer: str = Field(..., max_length=32)


class ProblemCardStatus(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    SOLVING = "SOLVING"
    SOLVED = "SOLVED"
    FAILED = "FAILED"
    REJECTED = "REJECTED"


class ProblemCardInfo(BaseSchemaModel):
    problem_card_id: int
    problem: ProblemId
    row: int
    column: int
    category_price: int
    category_name: str


class ProblemCardInfoForEditor(BaseSchemaModel):
    problem_card_id: int
    problem: ProblemInfoForEditor
    row: int
    column: int
    category_price: int
    category_name: str


class ProblemCardInfoForContestant(BaseSchemaModel):
    problem_card_id: int
    problem: ProblemId
    status: ProblemCardStatus
    is_open_for_buy: bool = Field(default=False)
    row: int
    column: int
    category_price: int
    category_name: str
