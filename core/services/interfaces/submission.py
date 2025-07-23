from typing import Protocol

from core.schemas.submission import SubmissionId


class ISubmissionService(Protocol):

    async def check_submission(
            self,
            user_id: int,
            selected_problem_id: int,
            answer: str,
    ) -> SubmissionId:
        ...

    # async def create_submission(
    #         self,
    #         user_id: int,
    #         selected_problem_id: int,
    #         answer: str,
    # ) -> SubmissionId:
    #     ...
