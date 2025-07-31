from backend.core.repository.crud.uow import get_unit_of_work
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
    permission_service = PermissionService(
        uow=await get_unit_of_work()
    )
    service = ContestService(
        uow=await get_unit_of_work(),
        permission_service=permission_service,
    )
    return await service.contest_standings(contest_id)
