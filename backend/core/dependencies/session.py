from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database.connection import get_session


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Провайдер асинхронной сессии SQLAlchemy для FastAPI.

    Оборачивает генератор `get_session()` и используется как зависимость
    (`Depends(get_async_session)`) в маршрутах и сервисах для работы с БД.

    Yields:
        AsyncSession: Экземпляр асинхронной сессии для взаимодействия с базой данных.
    """

    async for session in get_session():
        yield session
