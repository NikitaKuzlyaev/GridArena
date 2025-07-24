from typing import List, Sequence

from sqlalchemy import select

from core.dependencies.repository import get_repository
from core.models.submission import Submission
from core.repository.crud.base import BaseCRUDRepository
from core.utilities.loggers.log_decorator import log_calls


class SubmissionCRUDRepository(BaseCRUDRepository):

    @log_calls
    async def create_submission(
            self,
            selected_problem_id: int,
            answer: str,
    ) -> Submission:
        submission: Submission = (
            Submission(
                selected_problem_id=selected_problem_id,
                answer=answer,
            )
        )
        self.async_session.add(instance=submission)
        await self.async_session.commit()
        await self.async_session.refresh(instance=submission)
        return submission

    @log_calls
    async def get_submissions_of_selected_problem_by_id(
            self,
            selected_problem_id: int,
            filter_by_verdict: List[str] = None,
    ) -> Sequence[Submission]:
        stmt = select(Submission).where(
            Submission.selected_problem_id == selected_problem_id
        )

        if filter_by_verdict:
            stmt = stmt.where(Submission.verdict.in_(filter_by_verdict))

        res = await self.async_session.execute(stmt)
        return res.scalars().all()


submission_repo = get_repository(
    repo_type=SubmissionCRUDRepository
)
