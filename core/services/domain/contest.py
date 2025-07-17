from datetime import datetime
from typing import Sequence

from core.models import Contest
from core.repository.crud.contest import ContestCRUDRepository
from core.schemas.contest import ContestId, ContestShortInfo, ArrayContestShortInfo, ContestInfoForEditor
from core.services.interfaces.contest import IContestService
from core.services.interfaces.permission import IPermissionService
from core.utilities.exceptions.database import EntityDoesNotExist
from core.utilities.loggers.log_decorator import log_calls


class ContestService(IContestService):
    def __init__(
            self,
            contest_repo: ContestCRUDRepository,
            permission_service: IPermissionService,

    ):
        self.contest_repo = contest_repo
        self.permission_service = permission_service

    @log_calls
    async def create_full_contest(
            self,
            user_id: int,
            name: str,
            started_at: datetime,
            closed_at: datetime,
            start_points: int,
            number_of_slots_for_problems: int,
    ) -> ContestId:
        contest = (
            await self.contest_repo.create_full_contest(
                name=name,
                started_at=started_at,
                closed_at=closed_at,
                start_points=start_points,
                number_of_slots_for_problems=number_of_slots_for_problems,
            )
        )
        res = ContestId(contest_id=contest.id)

        return res

    @log_calls
    async def delete_contest(
            self,
            user_id,
            contest_id,
    ) -> None:
        contest: Contest = (
            await self.contest_repo.get_contest_by_id(
                contest_id=contest_id,
            )
        )
        if not contest:
            raise EntityDoesNotExist("contest not found")

        await self.contest_repo.delete_contest(
            contest_id=contest_id,
        )

        return None

    @log_calls
    async def contest_info_for_editor(
            self,
            user_id,
            contest_id,
    ) -> ContestInfoForEditor:
        contest: Contest = (
            await self.contest_repo.get_contest_by_id(
                contest_id=contest_id,
            )
        )
        if not contest:
            raise EntityDoesNotExist("contest not found")

        res = ContestInfoForEditor(
            contest_id=contest_id,
            name=contest.name,
            start_points=contest.start_points,
            number_of_slots_for_problems=contest.number_of_slots_for_problems,
            started_at=contest.started_at,
            closed_at=contest.closed_at,
        )
        return res

    @log_calls
    async def create_contest(
            self,
            user_id: int,
            name: str,
            started_at: datetime,
            closed_at: datetime,
            start_points: int,
            number_of_slots_for_problems: int,
    ) -> ContestId:
        contest = (
            await self.contest_repo.create_contest(
                name=name,
                started_at=started_at,
                closed_at=closed_at,
                start_points=start_points,
                number_of_slots_for_problems=number_of_slots_for_problems,
            )
        )
        res = ContestId(contest_id=contest.id)

        return res

    @log_calls
    async def update_contest(
            self,
            user_id: int,
            contest_id: int,
            name: str,
            started_at: datetime,
            closed_at: datetime,
            start_points: int,
            number_of_slots_for_problems: int,
    ) -> ContestId:
        contest: Contest | None = (
            await self.contest_repo.update_contest(
                contest_id=contest_id,
                name=name,
                started_at=started_at,
                closed_at=closed_at,
                start_points=start_points,
                number_of_slots_for_problems=number_of_slots_for_problems,
            )
        )
        if not contest:
            raise EntityDoesNotExist("")

        res = ContestId(contest_id=contest.id)
        return res

    @log_calls
    async def get_user_contests(
            self,
            user_id: int,
    ) -> ArrayContestShortInfo:
        contests: Sequence[Contest] = (
            await self.contest_repo.get_user_contests(
                user_id=user_id,
            )
        )
        res = ArrayContestShortInfo(
            body=[
                ContestShortInfo(
                    contest_id=contest.id,
                    name=contest.name,
                    started_at=contest.started_at,
                    closed_at=contest.closed_at,
                ) for contest in contests
            ]
        )
        return res
