from backend.core.models.contestant_log import ContestantLogLevelType
from backend.core.repository.crud.uow import UnitOfWork
from backend.core.schemas.contestant_log import LogMessage


class ContestantLogWriter:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def log_wrong_answer(self, contestant_id: int):
        await self.uow.contestant_log_repo.create_log(
            contestant_id=contestant_id,
            log_level=ContestantLogLevelType.INFO,
            content=LogMessage.wrong_answer(),
        )

    async def log_correct_answer(self, contestant_id: int):
        await self.uow.contestant_log_repo.create_log(
            contestant_id=contestant_id,
            log_level=ContestantLogLevelType.INFO,
            content=LogMessage.correct_answer(),
        )

    async def log_balance_increase(self, contestant_id: int, points: int):
        await self.uow.contestant_log_repo.create_log(
            contestant_id=contestant_id,
            log_level=ContestantLogLevelType.INFO,
            content=LogMessage.balance_increase(points=points),
        )
