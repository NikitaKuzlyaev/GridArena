from fastapi import Depends

from backend.core.dependencies.session import get_async_session
from backend.core.repository.crud.base import BaseCRUDRepository
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.repository.crud.contest import ContestCRUDRepository
from backend.core.repository.crud.contestant import ContestantCRUDRepository
from backend.core.repository.crud.domain import DomainCRUDRepository
from backend.core.repository.crud.permission import PermissionCRUDRepository
from backend.core.repository.crud.problem import ProblemCRUDRepository
from backend.core.repository.crud.problem_card import ProblemCardCRUDRepository
from backend.core.repository.crud.quiz import QuizFieldCRUDRepository
from backend.core.repository.crud.selected_problem import SelectedProblemCRUDRepository
from backend.core.repository.crud.submission import SubmissionCRUDRepository
from backend.core.repository.crud.transaction import TransactionCRUDRepository
from backend.core.repository.crud.user import UserCRUDRepository
from backend.core.utilities.loggers.log_decorator import log_calls


class UnitOfWork(BaseCRUDRepository):
    """
    Unit of Work — обёртка над сессией SQLAlchemy,
    агрегирующая все CRUD-репозитории и инкапсулирующая транзакции.

    Используется как единый вход в слой данных для сервисов,
    позволяя выполнять несколько операций в рамках одной сессии и транзакции.

    Пример использования:
        async with uow:
            user = await uow.user_repo.create(...)
            contest = await uow.contest_repo.get(...)
    """

    @log_calls
    def __init__(self, session: AsyncSession):
        """
        Инициализация uow с передачей сессии.
        Все CRUD-репозитории получают одну и ту же сессию.
        """
        self._session = session
        self.contest_repo: ContestCRUDRepository = ContestCRUDRepository(session)
        self.contestant_repo: ContestantCRUDRepository = ContestantCRUDRepository(session)
        self.selected_problem_repo: SelectedProblemCRUDRepository = SelectedProblemCRUDRepository(session)
        self.user_repo: UserCRUDRepository = UserCRUDRepository(session)
        self.permission_repo: PermissionCRUDRepository = PermissionCRUDRepository(session)
        self.problem_card_repo: ProblemCardCRUDRepository = ProblemCardCRUDRepository(session)
        self.problem_repo: ProblemCRUDRepository = ProblemCRUDRepository(session)
        self.quiz_field_repo: QuizFieldCRUDRepository = QuizFieldCRUDRepository(session)
        self.submission_repo: SubmissionCRUDRepository = SubmissionCRUDRepository(session)
        self.transaction_repo: TransactionCRUDRepository = TransactionCRUDRepository(session)
        self.domain_repo: DomainCRUDRepository = DomainCRUDRepository(session)

    async def __aenter__(self) -> "UnitOfWork":
        """
        Вход в контекстный менеджер. Начинается область действия транзакции.
        """
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Выход из контекста:
        - если была ошибка — выполняется rollback;
        - если всё прошло успешно — выполняется commit.
        """
        if exc_type:
            await self._session.rollback()
        else:
            await self._session.commit()

    @property
    def session(self) -> AsyncSession:
        """
        Доступ к сырой SQLAlchemy-сессии при необходимости.
        """
        return self._session


async def get_unit_of_work(
        session: AsyncSession = Depends(get_async_session),
) -> UnitOfWork:
    """
    Зависимость для FastAPI, создающая экземпляр UnitOfWork на каждый запрос.
    """
    return UnitOfWork(session)
