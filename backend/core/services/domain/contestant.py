from datetime import datetime, timezone, timedelta
from typing import Sequence, Tuple

from backend.core.models import Contest, Contestant, User, SelectedProblem
from backend.core.models.selected_problem import SelectedProblemStatusType
from backend.core.repository.crud.contest import ContestCRUDRepository
from backend.core.repository.crud.contestant import ContestantCRUDRepository
from backend.core.repository.crud.selected_problem import SelectedProblemCRUDRepository
from backend.core.repository.crud.user import UserCRUDRepository
from backend.core.schemas.contestant import (
    ArrayContestantInfoForEditor, ContestantInfo, ContestantId, ContestantPreviewInfo, ContestantInfoInContest)
from backend.core.services.interfaces.contestant import IContestantService
from backend.core.services.interfaces.permission import IPermissionService
from backend.core.utilities.exceptions.database import EntityDoesNotExist, EntityAlreadyExists
from backend.core.utilities.loggers.log_decorator import log_calls


class ContestantService(IContestantService):
    def __init__(
            self,
            contest_repo: ContestCRUDRepository,
            contestant_repo: ContestantCRUDRepository,
            permission_service: IPermissionService,
            selected_problem_repo: SelectedProblemCRUDRepository,
            user_repo: UserCRUDRepository,
    ):
        self.contest_repo = contest_repo
        self.contestant_repo = contestant_repo
        self.permission_service = permission_service
        self.selected_problem_repo = selected_problem_repo
        self.user_repo = user_repo

    @log_calls
    async def get_user_contestant_and_contest(
            self,
            user_id: int
    ) -> Tuple[User, Contestant, Contest]:
        user: User | None = (
            await self.user_repo.get_user_by_id(
                user_id=user_id,
            )
        )
        if not user:
            raise EntityDoesNotExist("user not found")

        contestant: Contestant | None = (
            await self.contestant_repo.get_contestant_by_user_id(
                user_id=user_id,
            )
        )
        if not contestant:
            raise EntityDoesNotExist("contestant was not found")

        contest: Contest | None = (
            await self.contest_repo.get_contest_by_id(
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
        try:
            user, contestant, contest = (
                await self.get_user_contestant_and_contest(
                    user_id=user_id,
                )
            )
            selected_problems: Sequence[SelectedProblem] = (
                await self.selected_problem_repo.get_selected_problem_of_contestant_by_id(
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
        try:
            user, contestant, contest = (
                await self.get_user_contestant_and_contest(
                    user_id=user_id,
                )
            )

            utc_plus_7 = timezone(timedelta(hours=7)) # какой кринж
            current_time = datetime.now(utc_plus_7) # todo: переделать нормально

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
        contestants: Sequence[Contestant] = (
            await self.contestant_repo.get_contestants_in_contest(
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
        contest: Contest | None = (
            await self.contest_repo.get_contest_by_id(
                contest_id=contest_id,
            )
        )
        if not contest:
            raise EntityDoesNotExist("contest not found")

        user: User | None = (
            await self.user_repo.get_user_by_username_and_domain(
                username=username,
                domain_number=contest_id,
            )
        )
        if user:
            raise EntityAlreadyExists("user already exists")

        user: User = (
            await self.user_repo.create_contest_user(
                domain_number=contest_id,
                username=username,
                password=password,
            )
        )
        contestant: Contestant = (
            await self.contestant_repo.create_contestant(
                user_id=user.id,
                name=name,
                points=points,
            )
        )
        res = ContestantId(
            contestant_id=contestant.id,
        )

        return res
