from datetime import (
    datetime,
    timezone,
    timedelta,
)
from typing import (
    Sequence,
    Tuple,
    Optional,
)

from backend.configuration.settings import settings
from backend.core.models import (
    Contest,
    Contestant,
    User,
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
from backend.core.schemas.permission import PermissionPromise
from backend.core.services.access_policies.contestant import ContestantAccessPolicy
from backend.core.services.interfaces.contestant import IContestantService

from backend.core.utilities.loggers.log_decorator import log_calls

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
            user: User = await self.uow.user_repo.get_user_by_id(user_id=user_id, )
            contestant: Contestant = await self.uow.contestant_repo.get_contestant_by_user_id(user_id=user_id, )

            total: int = await self.uow.contestant_log_repo.count_logs_by_contestant_id(contestant.id)

            logs: Sequence[ContestantLog] = await self.uow.contestant_log_repo.get_contestant_logs_in_contest(
                contestant_id=contestant.id,
                limit=limit,
                offset=offset,
            )

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

    @log_calls
    async def get_user_contestant_and_contest(
            self,
            user_id: int
    ) -> Tuple[User, Contestant, Contest]:
        async with self.uow:
            user: User = await self.uow.user_repo.get_user_by_id(user_id=user_id, )
            contestant: Contestant = await self.uow.contestant_repo.get_contestant_by_user_id(user_id=user_id, )
            contest: Contest = await self.uow.contest_repo.get_contest_by_id(contest_id=user.domain_number, )

            return user, contestant, contest

    @log_calls
    async def get_contestant_info_in_contest(
            self,
            user_id: int,
    ) -> ContestantInfoInContest:
        async with self.uow:
            # Проверка прав не требуется в текущей логике

            user, contestant, contest = await self.get_user_contestant_and_contest(user_id=user_id, )

            selected_problems: Sequence[SelectedProblem] = (
                await self.uow.selected_problem_repo.get_selected_problem_of_contestant_by_id(
                    contestant_id=contestant.id,
                    filter_by_status=[SelectedProblemStatusType.ACTIVE.value], )
            )
            res = ContestantInfoInContest(
                contestant_id=contestant.id,
                contestant_name=contestant.name,
                points=contestant.points,
                problems_current=len(selected_problems),
                problems_max=contest.number_of_slots_for_problems,
            )
            return res

    @log_calls
    async def get_contestant_preview(
            self,
            user_id: int,
    ) -> ContestantPreviewInfo:
        async with self.uow:
            # Проверка прав не требуется в текущей логике

            user, contestant, contest = await self.get_user_contestant_and_contest(user_id=user_id, )

            utc_plus_7 = timezone(timedelta(hours=7))  # какой кринж
            current_time = datetime.now(utc_plus_7)  # todo: переделать нормально

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

    @log_calls
    async def get_contestants_in_contest(
            self,
            user_id: int,
            contest_id: int,
    ) -> ArrayContestantInfoForEditor:
        async with self.uow:
            # Проверка прав доступа к ресурсу. Если доступа нет - выбросится исключение (raise_if_none=True)
            permission: PermissionPromise = (
                await self.access_policy.can_user_view_other_contestant(
                    uow=self.uow, user_id=user_id, contest_id=contest_id, raise_if_none=True, ))

            contestants: Sequence[Contestant] = (
                await self.uow.contestant_repo.get_contestants_in_contest(
                    contest_id, )
            )
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
