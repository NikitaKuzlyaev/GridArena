from fastapi import Depends

from core.dependencies.repository import get_repository
from core.repository.crud.contest import ContestCRUDRepository
from core.repository.crud.contestant import ContestantCRUDRepository
from core.repository.crud.selected_problem import SelectedProblemCRUDRepository
from core.repository.crud.user import UserCRUDRepository
from core.services.domain.contest import ContestService
from core.services.domain.contestant import ContestantService
from core.services.interfaces.contest import IContestService
from core.services.interfaces.contestant import IContestantService
from core.services.interfaces.permission import IPermissionService
from core.services.providers.permission import get_permission_service


def get_contestant_service(
        contest_repo: ContestCRUDRepository = Depends(get_repository(ContestCRUDRepository)),
        contestant_repo: ContestantCRUDRepository = Depends(get_repository(ContestantCRUDRepository)),
        permission_service: IPermissionService = Depends(get_permission_service),
        user_repo: UserCRUDRepository = Depends(get_repository(UserCRUDRepository)),
        selected_problem_repo: SelectedProblemCRUDRepository = Depends(get_repository(SelectedProblemCRUDRepository)),
) -> IContestantService:
    return ContestantService(
        contest_repo=contest_repo,
        contestant_repo=contestant_repo,
        permission_service=permission_service,
        user_repo=user_repo,
        selected_problem_repo=selected_problem_repo,
    )
