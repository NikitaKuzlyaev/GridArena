from backend.core.repository.crud.uow import UnitOfWork
from backend.core.schemas.problem import ProblemId

from backend.core.services.interfaces.problem import IProblemService
from backend.core.utilities.loggers.log_decorator import log_calls


class ProblemService(IProblemService):
    def __init__(
            self,
            uow: UnitOfWork,
    ):
        self.uow = uow

    @log_calls
    async def create_problem(
            self,
            user_id: int,
            statement: str,
            answer: str,
    ) -> ProblemId:
        raise NotImplementedError("method not implemented")

    @log_calls
    async def update_problem(
            self,
            user_id: int,
            problem_id: int,
            statement: str,
            answer: str,
    ) -> ProblemId:
        raise NotImplementedError("method not implemented")
