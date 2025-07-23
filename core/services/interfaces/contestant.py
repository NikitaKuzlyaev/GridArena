from typing import Protocol

from core.schemas.contestant import ArrayContestantInfoForEditor, ContestantId, ContestantPreviewInfo, \
    ContestantInfoInContest


class IContestantService(Protocol):

    async def get_contestant_info_in_contest(
            self,
            user_id: int,
    ) -> ContestantInfoInContest:
        ...

    async def get_contestant_preview(
            self,
            user_id: int,
    ) -> ContestantPreviewInfo:
        ...

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
