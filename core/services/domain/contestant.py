from datetime import datetime
from typing import Sequence

from core.models import Contest, Contestant, User
from core.repository.crud.contest import ContestCRUDRepository
from core.repository.crud.contestant import ContestantCRUDRepository
from core.repository.crud.user import UserCRUDRepository
from core.schemas.contest import ContestId, ContestShortInfo, ArrayContestShortInfo, ContestInfoForEditor
from core.schemas.contestant import ArrayContestantInfoForEditor, ContestantInfo, ContestantId
from core.services.interfaces.contest import IContestService
from core.services.interfaces.contestant import IContestantService
from core.services.interfaces.permission import IPermissionService
from core.utilities.exceptions.database import EntityDoesNotExist, EntityAlreadyExists
from core.utilities.loggers.log_decorator import log_calls


class ContestantService(IContestantService):
    def __init__(
            self,
            contest_repo: ContestCRUDRepository,
            contestant_repo: ContestantCRUDRepository,
            permission_service: IPermissionService,
            user_repo: UserCRUDRepository,

    ):
        self.contest_repo = contest_repo
        self.contestant_repo = contestant_repo
        self.permission_service = permission_service
        self.user_repo = user_repo

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
