from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from backend.configuration.settings import settings

# DATABASE_URL = os.getenv("DATABASE_DEBUG_URL")
# DATABASE_URL = "sqlite+aiosqlite:///./test.db"
# DATABASE_URL = "postgresql+asyncpg://postgres:2476@localhost:5432/quiz"
# from backend.configuration.settings import settings

DATABASE_URL = settings.async_main_database_url

engine = create_async_engine(DATABASE_URL, echo=False, future=True)

async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()


async def get_session() -> AsyncGenerator[Any, Any]:
    async with async_session() as session:
        yield session
