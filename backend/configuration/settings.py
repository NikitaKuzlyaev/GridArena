from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MAIN_ASYNC_DATABASE_URI: str = "postgresql+asyncpg://postgres:2476@localhost:5432/quiz"

    REDIS_KV_SIMPLE_CACHE_HOST: str = 'localhost'
    REDIS_KV_SIMPLE_CACHE_PORT: int = 6379
    REDIS_KV_SIMPLE_CACHE_DB: int = 0


settings = Settings()
