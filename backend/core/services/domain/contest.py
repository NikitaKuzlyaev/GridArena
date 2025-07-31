from datetime import datetime
from typing import Sequence

from backend.core.models import Contest
from backend.core.repository.crud.uow import UnitOfWork
from backend.core.schemas.contest import (
    ContestId,
    ContestShortInfo,
    ArrayContestShortInfo,
    ContestInfoForEditor,
    ContestStandings,
    ArrayContestantInStandings,
    ContestSubmissions,
    ArrayContestSubmissions,
)
from backend.core.services.interfaces.contest import IContestService
from backend.core.services.interfaces.permission import IPermissionService
from backend.core.utilities.exceptions.database import EntityDoesNotExist
from backend.core.utilities.loggers.log_decorator import log_calls


class ContestService(IContestService):
    def __init__(
            self,
            uow: UnitOfWork,
            permission_service: IPermissionService,
    ):
        self.uow = uow
        self.permission_service = permission_service

    @log_calls
    async def contest_submissions(
            self,
            contest_id: int,
            show_last_n_submissions: int = 30,
    ) -> ContestSubmissions:
        async with self.uow:
            contest: Contest | None = (
                await self.uow.contest_repo.get_contest_by_id(contest_id=contest_id)
            )
            if not contest:
                raise EntityDoesNotExist("contest not found")

            submissions_in_contest = (
                await self.uow.contest_repo.get_contest_submissions(
                    contest_id=contest_id,
                    show_last_n_submissions=show_last_n_submissions,
                )
            )

            res = ContestSubmissions(
                contest_id=contest.id,
                name=contest.name,
                started_at=contest.started_at,
                closed_at=contest.closed_at,
                submissions=ArrayContestSubmissions(
                    body=[i for i in submissions_in_contest],
                ),
                show_last_n_submissions=show_last_n_submissions,
            )

            return res

    @log_calls
    # @lazy_cache_optimizer.decorator_fabric(
    #     get_from_cache_not_later_than_s=5,
    #     result_cached_time_s=10,
    #     refresh_cache_if_ttl_less_than_s=5,
    # )
    async def contest_standings(
            self,
            contest_id: int,
    ) -> ContestStandings:
        async with self.uow:
            contest: Contest | None = (
                await self.uow.contest_repo.get_contest_by_id(contest_id=contest_id)
            )
            if not contest:
                raise EntityDoesNotExist("contest not found")

            contestant_in_standings = (
                await self.uow.contest_repo.get_contestant_in_standings(
                    contest_id=contest_id,
                )
            )

            res = ContestStandings(
                contest_id=contest.id,
                name=contest.name,
                started_at=contest.started_at,
                closed_at=contest.closed_at,
                standings=ArrayContestantInStandings(
                    body=[i for i in contestant_in_standings],
                ),
            )

            return res

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
        async with self.uow:
            contest = (
                await self.uow.contest_repo.create_full_contest(
                    name=name,
                    started_at=started_at,
                    closed_at=closed_at,
                    start_points=start_points,
                    number_of_slots_for_problems=number_of_slots_for_problems,
                )
            )
            res = ContestId(
                contest_id=contest.id,
            )
            return res

    @log_calls
    async def delete_contest(
            self,
            user_id: int,
            contest_id: int,
    ) -> None:
        async with self.uow:
            contest: Contest = (
                await self.uow.contest_repo.get_contest_by_id(
                    contest_id=contest_id,
                )
            )
            if not contest:
                raise EntityDoesNotExist("contest not found")

            await self.uow.contest_repo.delete_contest(
                contest_id=contest_id,
            )
            return None

    @log_calls
    async def contest_info_for_editor(
            self,
            user_id: int,
            contest_id: int,
    ) -> ContestInfoForEditor:
        async with self.uow:
            contest: Contest = (
                await self.uow.contest_repo.get_contest_by_id(
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
                rule_type=contest.rule_type,
                flag_user_can_have_negative_points=contest.flag_user_can_have_negative_points,
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
        async with self.uow:
            contest = (
                await self.uow.contest_repo.create_contest(
                    name=name,
                    started_at=started_at,
                    closed_at=closed_at,
                    start_points=start_points,
                    number_of_slots_for_problems=number_of_slots_for_problems,
                )
            )
            res = ContestId(
                contest_id=contest.id,
            )
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
            rule_type: str,
            flag_user_can_have_negative_points: bool,
    ) -> ContestId:
        async with self.uow:
            contest: Contest | None = (
                await self.uow.contest_repo.update_contest(
                    contest_id=contest_id,
                    name=name,
                    started_at=started_at,
                    closed_at=closed_at,
                    start_points=start_points,
                    number_of_slots_for_problems=number_of_slots_for_problems,
                    rule_type=rule_type,
                    flag_user_can_have_negative_points=flag_user_can_have_negative_points,
                )
            )
            if not contest:
                raise EntityDoesNotExist("")

            res = ContestId(
                contest_id=contest.id,
            )
            return res

    @log_calls
    async def get_user_contests(
            self,
            user_id: int,
    ) -> ArrayContestShortInfo:
        async with self.uow:
            contests: Sequence[Contest] = (
                await self.uow.contest_repo.get_user_contests(
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
