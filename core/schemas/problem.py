from core.schemas.base import BaseSchemaModel
from datetime import datetime
from typing import Optional

from pydantic import Field, validator, root_validator, model_validator


class ProblemId(BaseSchemaModel):
    problem_id: int

class ProblemUpdateRequest(BaseSchemaModel):
    problem_id: int
    statement: str = Field(..., max_length=2048)
    answer: str = Field(..., max_length=32)

