from fastapi import Depends

from backend.core.dependencies.session import get_async_session
from backend.core.repository.crud.base import BaseCRUDRepository
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.repository.crud.contest import ContestCRUDRepository
from backend.core.repository.crud.contestant import ContestantCRUDRepository
from backend.core.repository.crud.contestant_log import ContestantLogCRUDRepository
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
        Все CRUD-репозитории при инициализации получают одну и ту же сессию.
        """
        self._session = session
        self._repos = {}

    def _get_repo(self, repo_cls):
        if repo_cls not in self._repos:
            self._repos[repo_cls] = repo_cls(self._session)
        return self._repos[repo_cls]

    @property
    def contestant_log_repo(self) -> ContestantLogCRUDRepository:
        return self._get_repo(ContestantLogCRUDRepository)

    @property
    def contest_repo(self) -> ContestCRUDRepository:
        return self._get_repo(ContestCRUDRepository)

    @property
    def contestant_repo(self) -> ContestantCRUDRepository:
        return self._get_repo(ContestantCRUDRepository)

    @property
    def selected_problem_repo(self) -> SelectedProblemCRUDRepository:
        return self._get_repo(SelectedProblemCRUDRepository)

    @property
    def user_repo(self) -> UserCRUDRepository:
        return self._get_repo(UserCRUDRepository)

    @property
    def permission_repo(self) -> PermissionCRUDRepository:
        return self._get_repo(PermissionCRUDRepository)

    @property
    def problem_card_repo(self) -> ProblemCardCRUDRepository:
        return self._get_repo(ProblemCardCRUDRepository)

    @property
    def problem_repo(self) -> ProblemCRUDRepository:
        return self._get_repo(ProblemCRUDRepository)

    @property
    def quiz_field_repo(self) -> QuizFieldCRUDRepository:
        return self._get_repo(QuizFieldCRUDRepository)

    @property
    def submission_repo(self) -> SubmissionCRUDRepository:
        return self._get_repo(SubmissionCRUDRepository)

    @property
    def transaction_repo(self) -> TransactionCRUDRepository:
        return self._get_repo(TransactionCRUDRepository)

    @property
    def domain_repo(self) -> DomainCRUDRepository:
        return self._get_repo(DomainCRUDRepository)

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
