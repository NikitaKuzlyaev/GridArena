from datetime import datetime
from typing import Sequence

from pydantic import (
    Field,
    model_validator,
)

from backend.core.models.contest import ContestRuleType
from backend.core.models.submission import SubmissionVerdict
from backend.core.schemas.base import BaseSchemaModel


class ContestCreateRequest(BaseSchemaModel):
    name: str = Field(..., max_length=256)

    started_at: datetime
    closed_at: datetime

    start_points: int = Field(
        ..., ge=0, le=10000,
        description="Стартовый баланс",
    )
    number_of_slots_for_problems: int = Field(
        ..., ge=1, le=5,
        description="Сколько задач разрешено держать одновременно (1–5)",
    )

    @model_validator(mode='after')
    def check_dates(self) -> 'ContestCreateRequest':
        if self.started_at and self.closed_at and self.closed_at < self.started_at:
            raise ValueError("closed_at не может быть раньше started_at")
        return self


class ContestUpdateRequest(BaseSchemaModel):
    contest_id: int

    name: str = Field(..., max_length=256)

    started_at: datetime
    closed_at: datetime

    start_points: int = Field(
        ..., ge=0, le=10000,
        description="Стартовый баланс",
    )
    number_of_slots_for_problems: int = Field(
        ..., ge=1, le=5,
        description="Сколько задач разрешено держать одновременно (1–5)",
    )

    rule_type: ContestRuleType
    flag_user_can_have_negative_points: bool

    @model_validator(mode='after')
    def check_dates(self) -> 'ContestUpdateRequest':
        if self.started_at and self.closed_at and self.closed_at < self.started_at:
            raise ValueError("closed_at не может быть раньше started_at")
        return self


class ContestId(BaseSchemaModel):
    contest_id: int


class ContestShortInfo(BaseSchemaModel):
    contest_id: int
    name: str
    started_at: datetime
    closed_at: datetime


class ArrayContestShortInfo(BaseSchemaModel):
    body: Sequence[ContestShortInfo]


class ContestInfoForEditor(BaseSchemaModel):
    contest_id: int
    name: str
    start_points: int
    number_of_slots_for_problems: int
    started_at: datetime
    closed_at: datetime
    rule_type: ContestRuleType = Field(default=ContestRuleType.DEFAULT)
    flag_user_can_have_negative_points: bool = Field(default=False)


class ContestInfoForContestant(BaseSchemaModel):
    contest_id: int
    name: str
    started_at: datetime
    closed_at: datetime


class ContestantInStandings(BaseSchemaModel):
    contestant_id: int
    name: str
    points: int
    rank: int


class ProblemCardForSubmissionInfo(BaseSchemaModel):
    problem_card_id: int
    category_name: str
    category_price: int


class ContestSubmission(BaseSchemaModel):
    contestant_id: int
    contestant_name: str
    problem_card: ProblemCardForSubmissionInfo
    verdict: SubmissionVerdict


class ArrayContestantInStandings(BaseSchemaModel):
    body: Sequence[ContestantInStandings]


class ArrayContestSubmissions(BaseSchemaModel):
    body: Sequence[ContestSubmission]


class ContestStandings(BaseSchemaModel):
    contest_id: int
    name: str
    started_at: datetime
    closed_at: datetime
    standings: ArrayContestantInStandings
    use_cache: bool = Field(default=False)


class ContestSubmissions(BaseSchemaModel):
    contest_id: int
    name: str
    started_at: datetime
    closed_at: datetime
    submissions: ArrayContestSubmissions
    use_cache: bool = Field(default=False)
    show_last_n_submissions: int | None = Field(default=None)
