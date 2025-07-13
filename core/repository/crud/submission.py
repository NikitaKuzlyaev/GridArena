from datetime import datetime
from typing import Sequence, Tuple

from mako.testing.helpers import result_lines
from sqlalchemy import select, update, delete, and_, Row

from core.dependencies.repository import get_repository
from core.models import Contest, Permission, Problem
from core.models.permission import PermissionResourceType, PermissionActionType
from core.models.submission import Submission
from core.repository.crud.base import BaseCRUDRepository
from core.schemas.contest import ContestId
from core.utilities.loggers.log_decorator import log_calls


class SubmissionCRUDRepository(BaseCRUDRepository):

    @log_calls
    async def create_submission(
            self,
            selected_problem_id: int,
            answer: str,
    ) -> Submission:
        submission: Submission = (
            Submission(
                selected_problem_id=selected_problem_id,
                answer=answer,
            )
        )
        self.async_session.add(instance=submission)
        await self.async_session.commit()
        await self.async_session.refresh(instance=submission)
        return submission


submission_repo = get_repository(
    repo_type=SubmissionCRUDRepository
)
