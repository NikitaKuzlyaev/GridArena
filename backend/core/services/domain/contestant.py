from datetime import (
    datetime,
    timezone,
    timedelta,
)
from typing import (
    Sequence,
    Optional,
)

from backend.configuration.settings import settings
from backend.core.models import (
    Contest,
    Contestant,
    SelectedProblem,
    ContestantLog,
)
from backend.core.models.selected_problem import SelectedProblemStatusType
from backend.core.repository.crud.uow import UnitOfWork
from backend.core.schemas.contestant import (
    ArrayContestantInfoForEditor,
    ContestantInfo,
    ContestantPreviewInfo,
    ContestantInfoInContest,
)
from backend.core.schemas.contestant_log import (
    ContestantLogPaginatedResponse,
    ContestantLogInfo,
)
from backend.core.services.access_policies.contestant import ContestantAccessPolicy
from backend.core.services.interfaces.contestant import IContestantService
from backend.core.utilities.loggers.log_decorator import log_calls
from backend.core.utilities.server import get_server_time

UTC_PLUS = timezone(timedelta(hours=settings.SERVER_TIMEZONE_UTC_DELTA))


class ContestantService(IContestantService):
    def __init__(
            self,
            uow: UnitOfWork,
            access_policy: Optional[ContestantAccessPolicy] = None,
    ):
        self.uow = uow
        self.access_policy: ContestantAccessPolicy = access_policy or ContestantAccessPolicy()

    @log_calls
    async def get_contestant_logs_in_contest(
            self,
            user_id: int,
            offset: int = 0,
            limit: int = 20,
    ) -> ContestantLogPaginatedResponse:
        async with self.uow:
            user, contestant, _, _ = await self.uow.domain_repo.get_contestant_full_context(user_id=user_id, )

            total: int = await self.uow.contestant_log_repo.count_logs_by_contestant_id(contestant.id, )

            logs: Sequence[ContestantLog] = await self.uow.contestant_log_repo.get_contestant_logs_in_contest(
                contestant_id=contestant.id, limit=limit, offset=offset,
            )
            res = self._map_contestant_log_paginated_response(total, offset, limit, logs, )
            return res

    @log_calls
    async def get_contestant_info_in_contest(
            self,
            user_id: int,
    ) -> ContestantInfoInContest:
        async with self.uow:
            # Проверка прав не требуется в текущей логике

            user, contestant, contest, _ = await self.uow.domain_repo.get_contestant_full_context(user_id=user_id, )

            selected_problems: Sequence[SelectedProblem] = (
                await self.uow.selected_problem_repo.get_selected_problem_of_contestant_by_id(
                    contestant_id=contestant.id, filter_by_status=[SelectedProblemStatusType.ACTIVE.value], )
            )

            res = self._map_contestant_info_in_contest(contestant, selected_problems, contest, )
            return res

    @log_calls
    async def get_contestant_preview(
            self,
            user_id: int,
    ) -> ContestantPreviewInfo:
        async with self.uow:
            # Проверка прав не требуется в текущей логике

            user, contestant, contest, _ = await self.uow.domain_repo.get_contestant_full_context(user_id=user_id, )

            current_time = get_server_time(with_server_timezone=True)

            res = self._map_contestant_preview_info(contestant, contest, current_time, )
            return res

    @log_calls
    async def get_contestants_in_contest(
            self,
            user_id: int,
            contest_id: int,
    ) -> ArrayContestantInfoForEditor:
        async with self.uow:
            # Проверка прав доступа к ресурсу. Если доступа нет - выбросится исключение (raise_if_none=True)
            await self.access_policy.can_user_view_other_contestant(
                uow=self.uow, user_id=user_id, contest_id=contest_id, raise_if_none=True, )

            contestants: Sequence[Contestant] = await self.uow.contestant_repo.get_contestants_in_contest(contest_id, )

            res = self._map_array_contestant_int_editor(contestants, )
            return res

    @staticmethod
    def _map_contestant_info_in_contest(
            contestant: Contestant,
            selected_problems: Sequence[SelectedProblem],
            contest: Contest,
    ) -> ContestantInfoInContest:
        res = ContestantInfoInContest(
            contestant_id=contestant.id,
            contestant_name=contestant.name,
            points=contestant.points,
            problems_current=len(selected_problems),
            problems_max=contest.number_of_slots_for_problems,
        )
        return res

    @staticmethod
    def _map_contestant_log_paginated_response(
            total: int, offset: int, limit: int,
            logs: Sequence[ContestantLog],
    ) -> ContestantLogPaginatedResponse:
        res = ContestantLogPaginatedResponse(
            total=total,
            offset=offset,
            limit=limit,
            body=[
                ContestantLogInfo(
                    contestant_log_id=log.id,
                    log_level=log.level_type,
                    content=log.content,
                    created_at=log.created_at.astimezone(UTC_PLUS),
                ) for log in logs
            ],
        )
        return res

    @staticmethod
    def _map_contestant_preview_info(
            contestant: Contestant,
            contest: Contest,
            current_time: datetime,
    ) -> ContestantPreviewInfo:
        res = ContestantPreviewInfo(
            contestant_id=contestant.id,
            contestant_name=contestant.name,
            contest_id=contest.id,
            contest_name=contest.name,
            started_at=contest.started_at,
            closed_at=contest.closed_at,
            is_contest_open=contest.started_at < current_time < contest.closed_at,
        )
        return res

    @staticmethod
    def _map_array_contestant_int_editor(
            contestants: Sequence[Contestant],
    ) -> ArrayContestantInfoForEditor:
        res = ArrayContestantInfoForEditor(
            body=[
                ContestantInfo(
                    contestant_id=contestant.id,
                    name=contestant.name,
                    points=contestant.points
                ) for contestant in contestants
            ]
        )
        return res
