from fastapi import Depends

from core.dependencies.repository import get_repository
from core.repository.crud.contest import ContestCRUDRepository
from core.repository.crud.permission import PermissionCRUDRepository
from core.services.domain.contest import ContestService
from core.services.interfaces.contest import IContestService
from core.services.interfaces.permission import IPermissionService
from core.services.providers.permission import get_permission_service


def get_contest_service(
        contest_repo: ContestCRUDRepository = Depends(get_repository(ContestCRUDRepository)),
        permission_service: IPermissionService = Depends(get_permission_service),
) -> IContestService:
    return ContestService(
        contest_repo=contest_repo,
        permission_service=permission_service,
    )