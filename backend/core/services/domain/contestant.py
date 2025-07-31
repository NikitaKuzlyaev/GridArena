from datetime import (
    datetime,
    timezone,
    timedelta,
)
from typing import (
    Sequence,
    Tuple,
)

from backend.core.models import (
    Contest,
    Contestant,
    User,
    SelectedProblem,
)
from backend.core.models.selected_problem import SelectedProblemStatusType
from backend.core.repository.crud.uow import UnitOfWork
from backend.core.schemas.contestant import (
    ArrayContestantInfoForEditor,
    ContestantInfo,
    ContestantId,
    ContestantPreviewInfo,
    ContestantInfoInContest,
)
from backend.core.services.interfaces.contestant import IContestantService
from backend.core.services.interfaces.permission import IPermissionService
from backend.core.utilities.exceptions.database import (
    EntityDoesNotExist,
    EntityAlreadyExists,
)
from backend.core.utilities.loggers.log_decorator import log_calls


class ContestantService(IContestantService):
    def __init__(
            self,
            uow: UnitOfWork,
            permission_service: IPermissionService,
    ):
        self.permission_service = permission_service
        self.uow = uow

    @log_calls
    async def get_user_contestant_and_contest(
            self,
            user_id: int
    ) -> Tuple[User, Contestant, Contest]:
        async with self.uow:
            user: User | None = (
                await self.uow.user_repo.get_user_by_id(
                    user_id=user_id,
                )
            )
            if not user:
                raise EntityDoesNotExist("user not found")

            contestant: Contestant | None = (
                await self.uow.contestant_repo.get_contestant_by_user_id(
                    user_id=user_id,
                )
            )
            if not contestant:
                raise EntityDoesNotExist("contestant was not found")

            contest: Contest | None = (
                await self.uow.contest_repo.get_contest_by_id(
                    contest_id=user.domain_number,
                )
            )
            if not contest:
                raise EntityDoesNotExist("contest was not found")

            return user, contestant, contest

    @log_calls
    async def get_contestant_info_in_contest(
            self,
            user_id: int,
    ) -> ContestantInfoInContest:
        async with self.uow:
            try:
                user, contestant, contest = (
                    await self.get_user_contestant_and_contest(
                        user_id=user_id,
                    )
                )
                selected_problems: Sequence[SelectedProblem] = (
                    await self.uow.selected_problem_repo.get_selected_problem_of_contestant_by_id(
                        contestant_id=contestant.id,
                        filter_by_status=[SelectedProblemStatusType.ACTIVE.value],
                    )
                )
                res = ContestantInfoInContest(
                    contestant_id=contestant.id,
                    contestant_name=contestant.name,
                    points=contestant.points,
                    problems_current=len(selected_problems),
                    problems_max=contest.number_of_slots_for_problems,
                )
                return res

            except EntityDoesNotExist as e:
                raise EntityDoesNotExist(e.args[0])

    @log_calls
    async def get_contestant_preview(
            self,
            user_id: int,
    ) -> ContestantPreviewInfo:
        async with self.uow:
            try:
                user, contestant, contest = (
                    await self.get_user_contestant_and_contest(
                        user_id=user_id,
                    )
                )

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
            except EntityDoesNotExist as e:
                raise EntityDoesNotExist(e.args[0])

    @log_calls
    async def get_contestants_in_contest(
            self,
            user_id: int,
            contest_id: int,
    ) -> ArrayContestantInfoForEditor:
        async with self.uow:
            contestants: Sequence[Contestant] = (
                await self.uow.contestant_repo.get_contestants_in_contest(
                    contest_id,
                )
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

    @log_calls
    async def create_contestant(
            self,
            contest_id: int,
            username: str,
            password: str,
            name: str,
            points: int,
    ) -> ContestantId:
        async with self.uow:
            contest: Contest | None = (
                await self.uow.contest_repo.get_contest_by_id(
                    contest_id=contest_id,
                )
            )
            if not contest:
                raise EntityDoesNotExist("contest not found")

            user: User | None = (
                await self.uow.user_repo.get_user_by_username_and_domain(
                    username=username,
                    domain_number=contest_id,
                )
            )
            if user:
                raise EntityAlreadyExists("user already exists")

            user: User = (
                await self.uow.user_repo.create_contest_user(
                    domain_number=contest_id,
                    username=username,
                    password=password,
                )
            )
            contestant: Contestant = (
                await self.uow.contestant_repo.create_contestant(
                    user_id=user.id,
                    name=name,
                    points=points,
                )
            )
            res = ContestantId(
                contestant_id=contestant.id,
            )

            return res
