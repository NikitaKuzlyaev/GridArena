from fastapi import Depends

from core.dependencies.repository import get_repository
from core.repository.crud.contest import ContestCRUDRepository
from core.repository.crud.permission import PermissionCRUDRepository
from core.repository.crud.problem import ProblemCRUDRepository
from core.services.domain.contest import ContestService
from core.services.domain.problem import ProblemService
from core.services.interfaces.contest import IContestService
from core.services.interfaces.permission import IPermissionService
from core.services.interfaces.problem import IProblemService
from core.services.providers.permission import get_permission_service


def get_problem_service(
        problem_repo: ContestCRUDRepository = Depends(get_repository(ProblemCRUDRepository)),
) -> IProblemService:
    return ProblemService(
        problem_repo=problem_repo,
    )