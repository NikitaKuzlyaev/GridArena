from datetime import datetime
from typing import Sequence

# from core.dependencies.repository import get_repository, get_repository_manual
from core.models import Contest
from core.models.permission import PermissionResourceType, PermissionActionType
from core.repository.crud.contest import ContestCRUDRepository
from core.repository.crud.permission import PermissionCRUDRepository
from core.repository.crud.problem import ProblemCRUDRepository
from core.repository.crud.submission import SubmissionCRUDRepository
from core.schemas.contest import ContestId, ContestShortInfo
from core.schemas.problem import ProblemId
from core.schemas.submission import SubmissionId

from core.services.interfaces.contest import IContestService
from core.services.interfaces.permission import IPermissionService
from core.services.interfaces.problem import IProblemService
from core.services.interfaces.submission import ISubmissionService
from core.utilities.exceptions.database import EntityDoesNotExist
from core.utilities.loggers.log_decorator import log_calls


class SubmissionService(ISubmissionService):
    def __init__(
            self,
            submission_repo: SubmissionCRUDRepository,
    ):
        self.submission_repo = submission_repo

    @log_calls
    async def create_submission(
            self,
            user_id: int,
            statement: str,
            answer: str,
    ) -> SubmissionId:
        ...
