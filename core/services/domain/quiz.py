from datetime import datetime
from typing import Sequence

# from core.dependencies.repository import get_repository, get_repository_manual
from core.models import Contest, QuizField
from core.models.permission import PermissionResourceType, PermissionActionType
from core.repository.crud.contest import ContestCRUDRepository
from core.repository.crud.permission import PermissionCRUDRepository
from core.repository.crud.quiz import QuizFieldCRUDRepository
from core.schemas.contest import ContestId, ContestShortInfo
from core.schemas.quiz_field import QuizFieldId

from core.services.interfaces.contest import IContestService
from core.services.interfaces.permission import IPermissionService
from core.services.interfaces.quiz import IQuizFieldService
from core.utilities.exceptions.database import EntityDoesNotExist
from core.utilities.loggers.log_decorator import log_calls


class QuizFieldService(IQuizFieldService):
    def __init__(
            self,
            quiz_field_repo: QuizFieldCRUDRepository,
    ):
        self.quiz_field_repo = quiz_field_repo

    @log_calls
    async def create_quiz_field(
            self,
            contest_id: int,
            number_of_rows: int,
            number_of_columns: int,
    ) -> QuizFieldId:
        quiz_field: QuizField = (
            await self.quiz_field_repo.create_quiz_field(
                contest_id=contest_id,
                number_of_rows=number_of_rows,
                number_of_columns=number_of_columns,
            )
        )
        res = QuizFieldId(quiz_field_id=quiz_field.id)

        return res

    @log_calls
    async def update_quiz_field(
            self,
            quiz_field_id: int,
            number_of_rows: int,
            number_of_columns: int,
    ) -> QuizFieldId:
        ...
