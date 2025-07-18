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

class ContestantInCreate(BaseSchemaModel):
    username: str
    password: str
    name: str
    contest_id: int
    points: int

class ArrayContestantInfoForEditor(BaseSchemaModel):
    body: Sequence[ContestantInfo]
