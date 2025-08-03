from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SERVER_TIMEZONE_UTC_DELTA: int = 7  # UTC+7

    MAIN_ASYNC_DATABASE_URI: str = "postgresql+asyncpg://postgres:2476@localhost:5432/quiz"

    REDIS_KV_SIMPLE_CACHE_HOST: str = 'localhost'
    REDIS_KV_SIMPLE_CACHE_PORT: int = 6379
    REDIS_KV_SIMPLE_CACHE_DB: int = 0

    SECRET_KEY: str = "super-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 180
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 20

    RMQ_AMQP_URL: str = "amqp://guest:guest@localhost/"


settings = Settings()
