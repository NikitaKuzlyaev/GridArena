from typing import Sequence, List, Tuple

from sqlalchemy import select, Row

from core.dependencies.repository import get_repository
from core.models import SelectedProblem, ProblemCard, Problem
from core.models.selected_problem import SelectedProblemStatusType
from core.repository.crud.base import BaseCRUDRepository


class SelectedProblemCRUDRepository(BaseCRUDRepository):

    async def get_selected_problem_by_id(
            self,
            selected_problem_id: int,
    ) -> SelectedProblem | None:
        res = await self.async_session.execute(
            select(
                SelectedProblem,
            )
            .where(
                SelectedProblem.id == selected_problem_id,
            )
        )
        res = res.scalar_one_or_none()
        return res

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

    async def get_selected_problem_with_problem_card_and_problem_of_contestant_by_id(
            self,
            contestant_id: int,
    ) -> Sequence[Tuple[SelectedProblem, ProblemCard, Problem]]:
        res = await self.async_session.execute(
            select(
                SelectedProblem,
                ProblemCard,
                Problem
            )
            .join(
                ProblemCard,
                ProblemCard.id == SelectedProblem.problem_card_id
            )
            .join(
                Problem,
                Problem.id == ProblemCard.problem_id
            )
            .where(
                SelectedProblem.contestant_id == contestant_id
            )
        )
        return res.all()

    async def create_selected_problem(
            self,
            contestant_id: int,
            problem_card_id: int,
    ) -> SelectedProblem:
        selected_problem: SelectedProblem = (
            SelectedProblem(
                problem_card_id=problem_card_id,
                contestant_id=contestant_id,
                status=SelectedProblemStatusType.ACTIVE,
            )
        )
        self.async_session.add(instance=selected_problem)
        await self.async_session.commit()
        await self.async_session.refresh(instance=selected_problem)
        return selected_problem

    async def get_selected_problem_by_contestant_and_problem_card(
            self,
            contestant_id: int,
            problem_card_id: int,
    ) -> SelectedProblem | None:
        res = await self.async_session.execute(
            select(
                SelectedProblem,
            )
            .where(
                SelectedProblem.contestant_id == contestant_id,
                SelectedProblem.problem_card_id == problem_card_id,
            )
        )
        res = res.scalar_one_or_none()
        return res


selected_problem_repo = get_repository(
    repo_type=SelectedProblemCRUDRepository
)
