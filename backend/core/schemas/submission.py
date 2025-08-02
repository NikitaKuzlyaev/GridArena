from pydantic import Field

from backend.core.schemas.base import BaseSchemaModel


class SubmissionId(BaseSchemaModel):
    submission_id: int


class SubmissionCreateRequest(BaseSchemaModel):
    selected_problem_id: int
    answer: str = Field(..., min_length=1, max_length=32)
