from backend.core.dependencies.repository import get_repository_manual
from backend.core.repository.crud.contest import ContestCRUDRepository
from backend.core.repository.crud.permission import PermissionCRUDRepository
from backend.core.repository.crud.problem_card import ProblemCardCRUDRepository
from backend.core.repository.crud.quiz import QuizFieldCRUDRepository
from backend.core.repository.crud.user import UserCRUDRepository
from backend.core.schemas.contest import ContestStandings
from backend.core.services.domain.contest import ContestService
from backend.core.services.domain.permission import PermissionService
from backend.core.utilities.loggers.log_decorator import log_calls
from backend.core.utilities.methods.registry import function_registry



@function_registry.register_function(
    alias='backend.core.services.domain.contest.ContestService.contest_standings'
)
@log_calls
async def contest_standings_proxy(contest_id: int | None = None) -> ContestStandings:
    contest_repo = await get_repository_manual(ContestCRUDRepository)
    user_repo = await get_repository_manual(UserCRUDRepository)

    permission_service = PermissionService(
        permission_repo=await get_repository_manual(PermissionCRUDRepository),
        problem_card_repo=await get_repository_manual(ProblemCardCRUDRepository),
        quiz_field_repo=await get_repository_manual(QuizFieldCRUDRepository),
        user_repo=await get_repository_manual(UserCRUDRepository),
        contest_repo=await get_repository_manual(ContestCRUDRepository),
    )

    service = ContestService(
        contest_repo=contest_repo,
        permission_service=permission_service,
        user_repo=user_repo,
    )

    return await service.contest_standings(contest_id)
