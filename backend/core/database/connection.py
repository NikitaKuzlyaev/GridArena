from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

from backend.configuration.settings import settings

ASYNC_DATABASE_URI = settings.MAIN_ASYNC_DATABASE_URI
SYNC_DATABASE_URI = settings.MAIN_SYNC_DATABASE_URI

engine = create_async_engine(
    ASYNC_DATABASE_URI,
    echo=False,  # Логи выключены
    future=True,
)

engine_sync = create_engine(
    SYNC_DATABASE_URI,
    echo=False,
    future=True,
)

# Используем async_sessionmaker (SQLAlchemy 2.0+)
async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,  # это опционально, но можно оставить для совместимости
)

Base = declarative_base()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Асинхронный генератор сессий SQLAlchemy.

    Открывает новую сессию с базой данных, управляемую через контекстный менеджер.
    Используется как зависимость в FastAPI для работы с БД через AsyncSession.

    Yields:
        AsyncSession: Экземпляр асинхронной сессии SQLAlchemy.
    """

    async with async_session() as session:
        yield session
