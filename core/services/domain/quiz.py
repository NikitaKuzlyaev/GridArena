from datetime import datetime
from typing import Sequence

# from core.dependencies.repository import get_repository, get_repository_manual
from core.models import Contest
from core.models.permission import PermissionResourceType, PermissionActionType
from core.repository.crud.contest import ContestCRUDRepository
from core.repository.crud.permission import PermissionCRUDRepository
from core.repository.crud.quiz import QuizCRUDRepository
from core.schemas.contest import ContestId, ContestShortInfo
from core.schemas.quiz_field import QuizFieldId

from core.services.interfaces.contest import IContestService
from core.services.interfaces.permission import IPermissionService
from core.services.interfaces.quiz import IQuizService
from core.utilities.exceptions.database import EntityDoesNotExist
from core.utilities.loggers.log_decorator import log_calls


class QuizService(IQuizService):
    def __init__(
            self,
            quiz_repo: QuizCRUDRepository,
    ):
        self.quiz_repo = quiz_repo

    @log_calls
    async def create_quiz_field(
            self,
            contest_id: int,
            number_of_rows: int,
            number_of_columns: int,
    ) -> QuizFieldId:
        ...

    @log_calls
    async def update_quiz_field(
            self,
            quiz_field_id: int,
            number_of_rows: int,
            number_of_columns: int,
    ) -> QuizFieldId:
        ...
