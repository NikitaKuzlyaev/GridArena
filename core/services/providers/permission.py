from fastapi import Depends

from core.dependencies.repository import get_repository
from core.repository.crud.permission import PermissionCRUDRepository
from core.repository.crud.problem_card import ProblemCardCRUDRepository
from core.repository.crud.quiz import QuizFieldCRUDRepository
from core.services.domain.permission import PermissionService
from core.services.interfaces.permission import IPermissionService


def get_permission_service(
        permission_repo: PermissionCRUDRepository = Depends(get_repository(PermissionCRUDRepository)),
        problem_card_repo: ProblemCardCRUDRepository = Depends(get_repository(ProblemCardCRUDRepository)),
        quiz_field_repo: QuizFieldCRUDRepository = Depends(get_repository(QuizFieldCRUDRepository)),
) -> IPermissionService:
    return PermissionService(
        permission_repo=permission_repo,
        problem_card_repo=problem_card_repo,
        quiz_field_repo=quiz_field_repo,
    )
