from fastapi import Depends

from core.dependencies.repository import get_repository
from core.repository.crud.contest import ContestCRUDRepository
from core.repository.crud.permission import PermissionCRUDRepository
from core.repository.crud.quiz import QuizCRUDRepository
from core.services.domain.contest import ContestService
from core.services.domain.quiz import QuizService
from core.services.interfaces.contest import IContestService
from core.services.interfaces.permission import IPermissionService
from core.services.interfaces.quiz import IQuizService
from core.services.providers.permission import get_permission_service


def get_quiz_service(
        quiz_repo: QuizCRUDRepository = Depends(get_repository(QuizCRUDRepository)),
) -> IQuizService:
    return QuizService(
        quiz_repo=quiz_repo,
    )
