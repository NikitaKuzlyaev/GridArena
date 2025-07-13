from fastapi import Depends

from core.dependencies.repository import get_repository
from core.repository.crud.contest import ContestCRUDRepository
from core.repository.crud.permission import PermissionCRUDRepository
from core.services.domain.contest import ContestService
from core.services.domain.permission import PermissionService
from core.services.interfaces.contest import IContestService
from core.services.interfaces.permission import IPermissionService


def get_permission_service(
        permission_repo: PermissionCRUDRepository = Depends(get_repository(PermissionCRUDRepository)),
) -> IPermissionService:
    return PermissionService(
        permission_repo=permission_repo,
    )