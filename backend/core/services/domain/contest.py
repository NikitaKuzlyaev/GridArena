from typing import (
    Sequence,
    Optional,
)

from backend.core.models import (
    Contest,
    Contestant,
    User,
)
from backend.core.models.permission import (
    PermissionResourceType,
    PermissionActionType,
)
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
    ContestInfoForContestant,
    ContestSubmission,
    ContestantInStandings,
    ContestCreateRequest,
    ContestUpdateRequest,
)
from backend.core.schemas.contestant import ContestantId, ContestantInCreate
from backend.core.services.access_policies.contest import ContestAccessPolicy
from backend.core.services.interfaces.contest import IContestService
from backend.core.utilities.exceptions.database import (
    EntityAlreadyExists,
)
from backend.core.utilities.loggers.log_decorator import log_calls


class ContestService(IContestService):
    def __init__(
            self,
            uow: UnitOfWork,
            access_policy: Optional[ContestAccessPolicy] = None,
    ):
        self.uow = uow
        self.access_policy: ContestAccessPolicy = access_policy or ContestAccessPolicy()

    @log_calls
    async def contest_submissions(
            self,
            user_id: int,
            contest_id: int,
            show_user_only: bool = False,
            show_last_n_submissions: int = 30,
    ) -> ContestSubmissions:
        async with self.uow:
            await self.access_policy.can_user_view_contest_submissions(
                uow=self.uow, user_id=user_id, contest_id=contest_id, raise_if_none=True, )

            contest: Contest = (
                await self.uow.contest_repo.get_contest_by_id(contest_id=contest_id, )
            )
            submissions_in_contest: Sequence[ContestSubmission] = (
                await self.uow.contest_repo.get_contest_submissions(
                    contest_id=contest_id,
                    filter_by_user=(user_id,) if show_user_only else None,
                    show_last_n_submissions=show_last_n_submissions, )
            )
            res: ContestSubmissions = self._map_contest_submissions(
                contest, submissions_in_contest, show_last_n_submissions,
            )
            return res

    '''@lazy_cache_optimizer.decorator_fabric(
        get_from_cache_not_later_than_s=5,
        result_cached_time_s=10,
        refresh_cache_if_ttl_less_than_s=5,
    )'''

    @log_calls
    async def contest_standings(
            self,
            user_id: int,
            contest_id: int,
    ) -> ContestStandings:
        async with self.uow:
            await self.access_policy.can_user_view_contest_standing(
                uow=self.uow, user_id=user_id, contest_id=contest_id, raise_if_none=True, )

            contest: Contest = (
                await self.uow.contest_repo.get_contest_by_id(contest_id=contest_id)
            )
            contestant_in_standings: Sequence[ContestantInStandings] = (
                await self.uow.contest_repo.get_contestant_in_standings(
                    contest_id=contest_id, )
            )
            res: ContestStandings = self._map_contest_standings(
                contest, contestant_in_standings,
            )
            return res

    @log_calls
    async def create_full_contest(
            self,
            user_id: int,
            contest_data: ContestCreateRequest,
    ) -> ContestId:
        async with self.uow:
            await self.access_policy.can_user_create_contests(
                uow=self.uow, user_id=user_id, raise_if_none=True, )

            contest = await self.uow.contest_repo.create_full_contest(
                **contest_data.model_dump(),
            )
            for action in (PermissionActionType.EDIT, PermissionActionType.ADMIN):
                await self.uow.permission_repo.create_permission(
                    user_id=user_id,
                    resource_id=contest.id,
                    resource_type=PermissionResourceType.CONTEST.value,
                    permission_type=action.value,
                )

            res = ContestId(contest_id=contest.id, )
            return res

    async def contest_info_for_contestant(
            self,
            user_id: int,
    ) -> ContestInfoForContestant:
        async with self.uow:
            # todo: а почему не  async with self.uow as session ?
            #       и далее: await session.user_repo.get_user_by_id(user_id=user_id)

            user: User = await self.uow.user_repo.get_user_by_id(user_id=user_id)
            contest_id = user.domain_number

            await self.access_policy.can_user_view_contest(
                uow=self.uow, user_id=user_id, contest_id=contest_id, raise_if_none=True, )

            contest: Contest = (
                await self.uow.contest_repo.get_contest_by_id(contest_id=contest_id, )
            )

            res: ContestInfoForContestant = self._map_contest_info_contestant(contest)
            return res

    @log_calls
    async def delete_contest(
            self,
            user_id: int,
            contest_id: int,
    ) -> None:
        async with self.uow:
            await self.access_policy.can_user_delete_contest(
                uow=self.uow, user_id=user_id, contest_id=contest_id, raise_if_none=True, )

            await self.uow.contest_repo.delete_contest(contest_id=contest_id, )
            return None

    @log_calls
    async def contest_info_for_editor(
            self,
            user_id: int,
            contest_id: int,
    ) -> ContestInfoForEditor:
        async with self.uow:
            await self.access_policy.can_user_manage_contest(
                uow=self.uow, user_id=user_id, contest_id=contest_id, raise_if_none=True, )

            contest: Contest = (
                await self.uow.contest_repo.get_contest_by_id(contest_id=contest_id, )
            )

            res: ContestInfoForEditor = self._map_contest_info_editor(contest)
            return res

    @log_calls
    async def create_contest(
            self,
            user_id: int,
            contest_data: ContestCreateRequest,
    ) -> ContestId:
        async with self.uow:
            await self.access_policy.can_user_create_contests(
                uow=self.uow, user_id=user_id, raise_if_none=True, )

            contest: Contest = await self.uow.contest_repo.create_contest(**contest_data.model_dump(), )

            res = ContestId(contest_id=contest.id, )
            return res

    @log_calls
    async def update_contest(
            self,
            user_id: int,
            contest_data: ContestUpdateRequest,
    ) -> ContestId:
        async with self.uow:
            await self.access_policy.can_user_manage_contest(
                uow=self.uow, user_id=user_id, contest_id=contest_data.contest_id, raise_if_none=True, )

            contest: Contest = await self.uow.contest_repo.update_contest(
                **contest_data.model_dump(),
            )
            res = ContestId(contest_id=contest.id, )
            return res

    @log_calls
    async def get_user_contests(
            self,
            user_id: int,
    ) -> ArrayContestShortInfo:
        async with self.uow:
            await self.access_policy.can_user_create_contests(
                uow=self.uow, user_id=user_id, raise_if_none=True, )

            contests: Sequence[Contest] = (
                await self.uow.contest_repo.get_user_contests(user_id=user_id, )
            )

            res: ArrayContestShortInfo = self._map_array_contest_short_info(contests)
            return res

    @log_calls
    async def create_contestant(
            self,
            user_id: int,
            contestant_data: ContestantInCreate,
    ) -> ContestantId:
        async with self.uow:
            await self.access_policy.can_user_manage_contest(
                uow=self.uow, user_id=user_id, contest_id=contestant_data.contest_id, raise_if_none=True, )

            await self._ensure_user_does_not_exist(contestant_data.username, contestant_data.contest_id, )
            contestant = await self._create_user_and_contestant(contestant_data)

            res = ContestantId(contestant_id=contestant.id, )
            return res

    @staticmethod
    def _map_contest_submissions(
            contest: Contest,
            submissions_in_contest: Sequence[ContestSubmission],
            show_last_n_submissions: int,
    ) -> ContestSubmissions:
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

    @staticmethod
    def _map_contest_standings(
            contest: Contest,
            contestant_in_standings: Sequence[ContestantInStandings],
    ) -> ContestStandings:
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

    @staticmethod
    def _map_contest_info_contestant(
            contest: Contest,
    ) -> ContestInfoForContestant:
        res = ContestInfoForContestant(
            contest_id=contest.id,
            name=contest.name,
            started_at=contest.started_at,
            closed_at=contest.closed_at,
        )
        return res

    @staticmethod
    def _map_contest_info_editor(
            contest: Contest,
    ) -> ContestInfoForEditor:
        res = ContestInfoForEditor(
            contest_id=contest.id,
            name=contest.name,
            start_points=contest.start_points,
            number_of_slots_for_problems=contest.number_of_slots_for_problems,
            started_at=contest.started_at,
            closed_at=contest.closed_at,
            rule_type=contest.rule_type,
            flag_user_can_have_negative_points=contest.flag_user_can_have_negative_points,
        )
        return res

    @staticmethod
    def _map_array_contest_short_info(
            contests: Sequence[Contest],
    ) -> ArrayContestShortInfo:
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

    async def _ensure_user_does_not_exist(self, username: str, contest_id: int):
        existing = await self.uow.user_repo.get_user_by_username_and_domain(
            username=username,
            domain_number=contest_id,
        )
        if existing:
            raise EntityAlreadyExists("user already exists")

    async def _create_user_and_contestant(self, data: ContestantInCreate) -> Contestant:
        user = await self.uow.user_repo.create_contest_user(
            domain_number=data.contest_id,
            username=data.username,
            password=data.password,
        )
        contestant = await self.uow.contestant_repo.create_contestant(
            user_id=user.id,
            name=data.name,
            points=data.points,
            password=data.password,
        )
        return contestant
