from datetime import datetime
from typing import Protocol
from typing import Sequence

from core.models import Contest

from core.schemas.contest import ContestId, ContestCreateRequest, ContestShortInfo


class IContestService(Protocol):

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
    ) -> Sequence[ContestShortInfo]:
        ...