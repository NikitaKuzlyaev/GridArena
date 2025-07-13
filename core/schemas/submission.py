from core.schemas.base import BaseSchemaModel
from datetime import datetime
from typing import Optional

from pydantic import Field, validator, root_validator, model_validator


class SubmissionId(BaseSchemaModel):
    submission_id: int

class SubmissionCreateRequest(BaseSchemaModel):
    selected_problem_id: int
    answer: str = Field(..., max_length=32)