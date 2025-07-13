from datetime import datetime
from typing import Protocol
from typing import Sequence

from core.models import Contest

from core.schemas.contest import ContestId, ContestCreateRequest, ContestShortInfo
from core.schemas.problem import ProblemId
from core.schemas.submission import SubmissionId


class ISubmissionService(Protocol):

    async def create_submission(
            self,
            user_id: int,
            statement: str,
            answer: str,
    ) -> SubmissionId:
        ...
