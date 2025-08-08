from dataclasses import dataclass
from datetime import datetime
from typing import (
    Sequence,
    Annotated,
)

from pydantic import (
    Field,
    conint,
    constr,
)

from backend.core.schemas.base import BaseSchemaModel
from backend.core.utilities.server import get_server_time


@dataclass
class ModelConstrains:
    UsernameStr = Annotated[
        str,
        constr(min_length=1, max_length=64),
    ]
    PasswordStr = Annotated[
        str,
        constr(min_length=1, max_length=32),
    ]
    NameStr = Annotated[
        str,
        constr(min_length=1, max_length=256),
    ]
    PointsInt = Annotated[
        int,
        conint(ge=0, le=10000),
    ]


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
    username: ModelConstrains.UsernameStr
    password: ModelConstrains.PasswordStr
    name: ModelConstrains.NameStr
    contest_id: int
    points: ModelConstrains.PointsInt


class ContestantInfoForEditor(BaseSchemaModel):
    contestant_id: int
    user_id: int
    username: ModelConstrains.UsernameStr
    password: ModelConstrains.PasswordStr
    contestant_name: ModelConstrains.NameStr
    points: ModelConstrains.PointsInt


class ContestantPatchRequest(BaseSchemaModel):
    contestant_id: int
    username: ModelConstrains.UsernameStr
    password: ModelConstrains.PasswordStr
    contestant_name: ModelConstrains.NameStr
    points: ModelConstrains.PointsInt
