from datetime import datetime
from typing import Sequence

from pydantic import Field

from backend.core.schemas.base import BaseSchemaModel
from backend.core.utilities.server import get_server_time


class ContestantId(BaseSchemaModel):
    contestant_id: int


class ContestantInfo(BaseSchemaModel):
    contestant_id: int
    name: str
    points: int


class ArrayContestantInfoForEditor(BaseSchemaModel):
    body: Sequence[ContestantInfo]


class ContestantPreviewInfo(BaseSchemaModel):
    contestant_id: int
    contestant_name: str
    contest_id: int
    contest_name: str
    started_at: datetime
    closed_at: datetime
    is_contest_open: bool
    # Серверное время. (Присваивается автоматически при создании экземпляра модели)
    server_time: datetime = Field(
        default_factory=lambda: get_server_time(with_server_timezone=True)
    )


class ContestantInfoInContest(BaseSchemaModel):
    contestant_id: int
    contestant_name: str
    points: int
    problems_current: int
    problems_max: int
    # Серверное время. (Присваивается автоматически при создании экземпляра модели)
    server_time: datetime = Field(
        default_factory=lambda: get_server_time(with_server_timezone=True)
    )


class ContestantInCreate(BaseSchemaModel):
    username: str
    password: str
    name: str
    contest_id: int
    points: int
