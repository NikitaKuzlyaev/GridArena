from datetime import datetime
from typing import Sequence

from core.schemas.base import BaseSchemaModel
from core.schemas.problem import ProblemInfoForContestant


class SelectedProblemId(BaseSchemaModel):
    selected_problem_id: int


class SelectedProblemBuyRequest(BaseSchemaModel):
    problem_card_id: int


class SelectedProblemInfoForContestant(BaseSchemaModel):
    selected_problem_id: int
    problem_card_id: int
    problem: ProblemInfoForContestant
    created_at: datetime

class ArraySelectedProblemInfoForContestant(BaseSchemaModel):
    body: Sequence[SelectedProblemInfoForContestant]