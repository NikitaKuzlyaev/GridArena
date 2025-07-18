from datetime import datetime
from typing import Protocol

from core.models import Contestant
from core.schemas.contest import ContestId, ContestInfoForEditor, \
    ContestInfoForContestant, ArrayContestShortInfo
from core.schemas.contestant import ArrayContestantInfoForEditor, ContestantId


class IContestantService(Protocol):

    async def get_contestants_in_contest(
            self,
            user_id: int,
            contest_id: int,
    ) -> ArrayContestantInfoForEditor:
        ...

    async def create_contestant(
            self,
            contest_id: int,
            username: str,
            password: str,
            name: str,
            points: int,
    ) -> ContestantId:
        ...
