from fastapi import Depends

from backend.core.dependencies.repository import get_repository
from backend.core.repository.crud.contest import ContestCRUDRepository
from backend.core.repository.crud.permission import PermissionCRUDRepository
from backend.core.repository.crud.problem_card import ProblemCardCRUDRepository
from backend.core.repository.crud.quiz import QuizFieldCRUDRepository
from backend.core.repository.crud.user import UserCRUDRepository
from backend.core.services.domain.permission import PermissionService
from backend.core.services.interfaces.permission import IPermissionService


def get_permission_service(
        permission_repo: PermissionCRUDRepository = Depends(get_repository(PermissionCRUDRepository)),
        problem_card_repo: ProblemCardCRUDRepository = Depends(get_repository(ProblemCardCRUDRepository)),
        quiz_field_repo: QuizFieldCRUDRepository = Depends(get_repository(QuizFieldCRUDRepository)),
        user_repo: UserCRUDRepository = Depends(get_repository(UserCRUDRepository)),
        contest_repo: ContestCRUDRepository = Depends(get_repository(ContestCRUDRepository)),
) -> IPermissionService:
    return PermissionService(
        permission_repo=permission_repo,
        problem_card_repo=problem_card_repo,
        quiz_field_repo=quiz_field_repo,
        user_repo=user_repo,
        contest_repo=contest_repo,
    )
