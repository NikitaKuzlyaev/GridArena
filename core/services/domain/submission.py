from core.repository.crud.submission import SubmissionCRUDRepository
from core.schemas.submission import SubmissionId

from core.services.interfaces.submission import ISubmissionService
from core.utilities.loggers.log_decorator import log_calls


class SubmissionService(ISubmissionService):
    def __init__(
            self,
            submission_repo: SubmissionCRUDRepository,
    ):
        self.submission_repo = submission_repo

    @log_calls
    async def create_submission(
            self,
            user_id: int,
            statement: str,
            answer: str,
    ) -> SubmissionId:
        ...
