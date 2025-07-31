from typing import (
    List,
    Sequence,
)

from sqlalchemy import (
    select,
    func,
)

from backend.core.models.submission import Submission
from backend.core.repository.crud.base import BaseCRUDRepository
from backend.core.utilities.loggers.log_decorator import log_calls


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
        await self.async_session.flush()
        # await self.async_session.commit()
        # await self.async_session.refresh(instance=submission)
        return submission

    async def get_attempts_count_grouped_by_selected_problem_id(
            self,
            selected_problem_ids: list[int],
            filter_by_verdict: List[str] = None,
    ) -> dict[int, int]:
        stmt = select(
            Submission.selected_problem_id,
            func.count().label("attempt_count")
        ).where(Submission.selected_problem_id.in_(selected_problem_ids))

        if filter_by_verdict:
            stmt = stmt.where(Submission.verdict.in_(filter_by_verdict))

        stmt = stmt.group_by(Submission.selected_problem_id)
        result = await self.async_session.execute(stmt)

        rows = result.all()
        return {selected_problem_id: count for selected_problem_id, count in rows}

    @log_calls
    async def get_submissions_of_selected_problem_by_id(
            self,
            selected_problem_id: int,
            filter_by_verdict: List[str] = None,
    ) -> Sequence[Submission]:
        stmt = (
            select(Submission)
            .where(Submission.selected_problem_id == selected_problem_id)
        )

        if filter_by_verdict:
            stmt = stmt.where(Submission.verdict.in_(filter_by_verdict))

        res = await self.async_session.execute(stmt)
        return res.scalars().all()


"""
Пример вызова

submission_repo = get_repository(
    repo_type=SubmissionCRUDRepository
)
"""
