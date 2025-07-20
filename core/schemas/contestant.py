from datetime import datetime
from typing import Sequence

from pydantic import Field, model_validator

from core.schemas.base import BaseSchemaModel


class ContestantId(BaseSchemaModel):
    contestant_id: int


class ContestantInfo(BaseSchemaModel):
    contestant_id: int
    name: str
    points: int


class ContestantPreviewInfo(BaseSchemaModel):
    contestant_id: int
    contestant_name: str
    contest_id: int
    contest_name: str
    started_at: datetime
    closed_at: datetime
    is_contest_open: bool


class ContestantInfoInContest(BaseSchemaModel):
    contestant_id: int
    contestant_name: str
    points: int
    problems_current: int
    problems_max: int


class ContestantInCreate(BaseSchemaModel):
    username: str
    password: str
    name: str
    contest_id: int
    points: int


class ArrayContestantInfoForEditor(BaseSchemaModel):
    body: Sequence[ContestantInfo]
