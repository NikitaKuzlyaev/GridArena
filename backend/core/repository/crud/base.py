from sqlalchemy.ext.asyncio import AsyncSession as SQLAlchemyAsyncSession


class BaseCRUDRepository:
    """
    Базовый класс для CRUD-репозиториев.

    Хранит асинхронную сессию SQLAlchemy, используемую для работы с базой данных.

    Attributes:
        async_session (SQLAlchemyAsyncSession): Асинхронная сессия для выполнения запросов.
    """

    def __init__(
            self,
            async_session: SQLAlchemyAsyncSession
    ):
        self.async_session = async_session
