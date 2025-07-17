from fastapi import Depends

from core.dependencies.repository import get_repository
from core.repository.crud.problem import ProblemCRUDRepository
from core.services.domain.problem import ProblemService
from core.services.interfaces.problem import IProblemService


def get_problem_service(
        problem_repo: ProblemCRUDRepository = Depends(get_repository(ProblemCRUDRepository)),
) -> IProblemService:
    return ProblemService(
        problem_repo=problem_repo,
    )
