from fastapi import Depends

from core.dependencies.repository import get_repository
from core.repository.crud.contest import ContestCRUDRepository
from core.repository.crud.permission import PermissionCRUDRepository
from core.repository.crud.problem import ProblemCRUDRepository
from core.repository.crud.problem_card import ProblemCardCRUDRepository
from core.services.domain.contest import ContestService
from core.services.domain.problem import ProblemService
from core.services.domain.problem_card import ProblemCardService
from core.services.interfaces.contest import IContestService
from core.services.interfaces.permission import IPermissionService
from core.services.interfaces.problem import IProblemService
from core.services.interfaces.problem_card import IProblemCardService
from core.services.providers.permission import get_permission_service


def get_problem_card_service(
        problem_card_repo: ProblemCardCRUDRepository = Depends(get_repository(ProblemCardCRUDRepository)),
) -> IProblemCardService:
    return ProblemCardService(
        problem_card_repo=problem_card_repo,
    )