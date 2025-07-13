from core.schemas.base import BaseSchemaModel
from datetime import datetime
from typing import Optional

from pydantic import Field, validator, root_validator, model_validator


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

    @model_validator(mode='after')
    def check_dates(self) -> 'ContestUpdateRequest':
        if self.started_at and self.closed_at and self.closed_at < self.started_at:
            raise ValueError("closed_at не может быть раньше started_at")
        return self


class ContestId(BaseSchemaModel):
    contest_id: int


class ContestShortInfo(BaseSchemaModel):
    contest_id: int
    name: str = Field(..., max_length=256)
    started_at: datetime
    closed_at: datetime
