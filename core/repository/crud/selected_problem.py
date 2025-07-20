from typing import Sequence, List

from sqlalchemy import select, update

from core.dependencies.repository import get_repository
from core.models import QuizField, SelectedProblem
from core.repository.crud.base import BaseCRUDRepository


class SelectedProblemCRUDRepository(BaseCRUDRepository):

    async def get_selected_problem_of_contestant_by_id(
            self,
            contestant_id: int,
            filter_by_status: List[str] = None,
    ) -> Sequence[SelectedProblem]:
        stmt = select(SelectedProblem).where(
            SelectedProblem.contestant_id == contestant_id
        )

        if filter_by_status:
            stmt = stmt.where(SelectedProblem.status.in_(filter_by_status))

        res = await self.async_session.execute(stmt)
        return res.scalars().all()


selected_problem_repo = get_repository(
    repo_type=SelectedProblemCRUDRepository
)
