from enum import Enum

from core.schemas.base import BaseSchemaModel
from datetime import datetime
from typing import Optional

from pydantic import Field, validator, root_validator, model_validator


class ProblemCard(BaseSchemaModel):
    problem_card_id: int


class ProblemCardStatus(str, Enum):
    CLOSED = "CLOSED"
    SOLVING = "SOLVING"
    SOLVED = "SOLVED"
    FAILED = "FAILED"


class ProblemCardInfoForEditor(BaseSchemaModel):
    problem_card_id: int
    problem: ProblemInfoForEditor


class ProblemCardInfoForContestant(BaseSchemaModel):
    problem_card_id: int
    problem: ProblemInfoForContestant
    status: ProblemCardStatus
