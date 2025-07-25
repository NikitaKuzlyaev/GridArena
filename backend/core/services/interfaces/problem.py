from typing import Protocol

from backend.core.schemas.problem import ProblemId


class IProblemService(Protocol):

    async def create_problem(
            self,
            statement: str,
            answer: str,
    ) -> ProblemId:
        ...

    async def update_problem(
            self,
            problem_id: int,
            statement: str,
            answer: str,
    ) -> ProblemId:
        ...
