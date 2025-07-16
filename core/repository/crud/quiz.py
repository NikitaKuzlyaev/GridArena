from datetime import datetime
from typing import Sequence, Tuple

from mako.testing.helpers import result_lines
from sqlalchemy import select, update, delete, and_, Row

from core.dependencies.repository import get_repository
from core.models import Contest, Permission, QuizField
from core.models.permission import PermissionResourceType, PermissionActionType
from core.repository.crud.base import BaseCRUDRepository
from core.schemas.contest import ContestId
from core.utilities.loggers.log_decorator import log_calls


class QuizFieldCRUDRepository(BaseCRUDRepository):

    async def create_quiz_field(
            self,
            contest_id: int,
            number_of_rows: int,
            number_of_columns: int,
    ) -> QuizField:
        quiz_field: QuizField = (
            QuizField(
                contest_id=contest_id,
                number_of_rows=number_of_rows,
                number_of_columns=number_of_columns,
            )
        )
        self.async_session.add(instance=quiz_field)
        await self.async_session.commit()
        await self.async_session.refresh(instance=quiz_field)
        return quiz_field


quiz_field_repo = get_repository(
    repo_type=QuizFieldCRUDRepository
)
