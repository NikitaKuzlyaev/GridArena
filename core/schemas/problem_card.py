from enum import Enum

from core.schemas.base import BaseSchemaModel
from datetime import datetime
from typing import Optional

from pydantic import Field, validator, root_validator, model_validator

from core.schemas.problem import ProblemInfoForEditor, ProblemInfoForContestant, ProblemId


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
    CLOSED = "CLOSED"
    SOLVING = "SOLVING"
    SOLVED = "SOLVED"
    FAILED = "FAILED"


class ProblemCardInfo(BaseSchemaModel):
    problem_card_id: int
    problem: ProblemId #ProblemInfoForEditor
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
