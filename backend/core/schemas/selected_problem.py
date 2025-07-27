from datetime import datetime
from typing import Sequence

from backend.core.models.contest import ContestRuleType
from backend.core.schemas.base import BaseSchemaModel
from backend.core.schemas.problem import ProblemInfoForContestant


class SelectedProblemId(BaseSchemaModel):
    selected_problem_id: int


class SelectedProblemBuyRequest(BaseSchemaModel):
    problem_card_id: int


class SelectedProblemInfoForContestant(BaseSchemaModel):
    selected_problem_id: int
    problem_card_id: int
    problem: ProblemInfoForContestant
    category_name: str
    category_price: int
    created_at: datetime
    attempts_remaining: int | None = None


class ArraySelectedProblemInfoForContestant(BaseSchemaModel):
    body: Sequence[SelectedProblemInfoForContestant]
    rule_type: ContestRuleType
    max_attempts_for_problem: int | None = None
