from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from backend.configuration.settings import settings

DATABASE_URI = settings.MAIN_ASYNC_DATABASE_URI

engine = create_async_engine(DATABASE_URI, echo=False, future=True)

async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()


async def get_session() -> AsyncGenerator[Any, Any]:
    async with async_session() as session:
        yield session
