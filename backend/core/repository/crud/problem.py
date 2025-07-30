from sqlalchemy import (
    select,
    update,
)

from backend.core.dependencies.repository import get_repository
from backend.core.models import Problem
from backend.core.repository.crud.base import BaseCRUDRepository
from backend.core.utilities.loggers.log_decorator import log_calls


class ProblemCRUDRepository(BaseCRUDRepository):

    @log_calls
    async def get_problem_by_id(
            self,
            problem_id: int,
    ) -> Problem | None:
        res = await self.async_session.execute(
            select(Problem)
            .where(Problem.id == problem_id)
        )
        res = res.scalar_one_or_none()
        return res

    @log_calls
    async def create_problem(
            self,
            statement: str,
            answer: str,
    ) -> Problem:
        problem: Problem = (
            Problem(
                statement=statement,
                answer=answer,
            )
        )
        self.async_session.add(instance=problem)
        await self.async_session.commit()
        await self.async_session.refresh(instance=problem)
        return problem

    @log_calls
    async def update_problem(
            self,
            problem_id: int,
            statement: str,
            answer: str,
    ) -> Problem | None:
        await self.async_session.execute(
            update(Problem)
            .where(Problem.id == problem_id)
            .values(
                statement=statement,
                answer=answer
            )
            .execution_options(synchronize_session="fetch")
        )
        await self.async_session.commit()

        result = await self.async_session.execute(
            select(Problem)
            .where(Problem.id == problem_id)
        )
        return result.scalar_one_or_none()


problem_repo = get_repository(
    repo_type=ProblemCRUDRepository
)
