from datetime import datetime
from typing import Protocol

from core.models.contest import ContestRuleType
from core.schemas.contest import ContestId, ContestInfoForEditor, \
    ContestInfoForContestant, ArrayContestShortInfo


class IContestService(Protocol):

    async def create_full_contest(
            self,
            user_id: int,
            name: str,
            started_at: datetime,
            closed_at: datetime,
            start_points: int,
            number_of_slots_for_problems: int,
    ) -> ContestId:
        ...

    async def contest_info_for_contestant(
            self,
            user_id,
            contest_id,
    ) -> ContestInfoForContestant:
        ...

    async def delete_contest(
            self,
            user_id,
            contest_id,
    ) -> None:
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
            rule_type: str,
            flag_user_can_have_negative_points: bool,
    ) -> ContestId:
        ...

    async def get_user_contests(
            self,
            user_id: int,
    ) -> ArrayContestShortInfo:
        ...
