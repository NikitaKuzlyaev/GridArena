from datetime import datetime
from typing import Sequence

# from core.dependencies.repository import get_repository, get_repository_manual
from core.models import Contest, Problem
from core.models.permission import PermissionResourceType, PermissionActionType
from core.repository.crud.contest import ContestCRUDRepository
from core.repository.crud.permission import PermissionCRUDRepository
from core.repository.crud.problem import ProblemCRUDRepository
from core.schemas.contest import ContestId, ContestShortInfo
from core.schemas.problem import ProblemId

from core.services.interfaces.contest import IContestService
from core.services.interfaces.permission import IPermissionService
from core.services.interfaces.problem import IProblemService
from core.utilities.exceptions.database import EntityDoesNotExist
from core.utilities.loggers.log_decorator import log_calls


class ProblemService(IProblemService):
    def __init__(
            self,
            problem_repo: ProblemCRUDRepository,
    ):
        self.problem_repo = problem_repo

    @log_calls
    async def create_problem(
            self,
            statement: str,
            answer: str,
    ) -> ProblemId:
        problem: Problem = (
            await self.problem_repo.create_problem(
                statement=statement,
                answer=answer,
            )
        )
        res = ProblemId(problem_id=problem.id)

        return res

    @log_calls
    async def update_problem(
            self,
            problem_id: int,
            statement: str,
            answer: str,
    ) -> ProblemId:
        ...