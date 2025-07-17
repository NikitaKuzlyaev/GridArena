from core.models import Problem
from core.repository.crud.problem import ProblemCRUDRepository
from core.schemas.problem import ProblemId

from core.services.interfaces.problem import IProblemService
from core.utilities.loggers.log_decorator import log_calls


class ProblemService(IProblemService):
    def __init__(
            self,
            problem_repo: ProblemCRUDRepository,
    ):
        self.problem_repo = problem_repo

    @log_calls
    async def create_problem(
            self,
            statement: str,
            answer: str,
    ) -> ProblemId:
        problem: Problem = (
            await self.problem_repo.create_problem(
                statement=statement,
                answer=answer,
            )
        )
        res = ProblemId(problem_id=problem.id)

        return res

    @log_calls
    async def update_problem(
            self,
            problem_id: int,
            statement: str,
            answer: str,
    ) -> ProblemId:
        ...
