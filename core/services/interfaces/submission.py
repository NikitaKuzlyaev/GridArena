from typing import Protocol

from core.schemas.submission import SubmissionId


class ISubmissionService(Protocol):

    async def create_submission(
            self,
            user_id: int,
            statement: str,
            answer: str,
    ) -> SubmissionId:
        ...
