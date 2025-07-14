from datetime import datetime
from typing import Protocol
from typing import Sequence

from core.models import Contest

from core.schemas.contest import ContestId, ContestCreateRequest, ContestShortInfo, ContestInfoForEditor, \
    ContestInfoForContestant, ArrayContestShortInfo


class IContestService(Protocol):
    async def contest_info_for_contestant(
            self,
            user_id,
            contest_id,
    ) -> ContestInfoForContestant:
        ...

    async def contest_info_for_editor(
            self,
            user_id,
            contest_id,
    ) -> ContestInfoForEditor:
        ...

    async def create_contest(
            self,
            user_id: int,
            name: str,
            started_at: datetime,
            closed_at: datetime,
            start_points: int,
            number_of_slots_for_problems: int,
    ) -> ContestId:
        ...

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
        ...

    async def get_user_contests(
            self,
            user_id: int,
    ) -> ArrayContestShortInfo:
        ...
