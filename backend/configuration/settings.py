from enum import Enum
from pathlib import Path

from pydantic_settings import BaseSettings


class Environment(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"


current_environment = Environment.DEVELOPMENT


class Settings(BaseSettings):
    class Config:
        env_file = str(Path(__file__).parent / f".env.{current_environment.value}")
        env_file_encoding = "utf-8"
        case_sensitive = False

    ENVIRONMENT: str = current_environment.value

    """
    Далее перечислены значения по умолчанию.
    
    Сейчас совпадают с окружением `DEVELOPMENT`
    """

    SERVER_TIMEZONE_UTC_DELTA: int = 7  # UTC+7

    MAIN_ASYNC_DATABASE_URI: str = "postgresql+asyncpg://postgres:2476@localhost:5432/quiz"
    MAIN_SYNC_DATABASE_URI: str = "postgresql://postgres:2476@localhost:5432/quiz"

    REDIS_KV_SIMPLE_CACHE_HOST: str = 'localhost'
    REDIS_KV_SIMPLE_CACHE_PORT: int = 6379
    REDIS_KV_SIMPLE_CACHE_DB: int = 0

    #  Fernet key must be 32 url-safe base64-encoded bytes.
    FERNET_KEY: str = "vHf2zp7vofWyFNhkfbR1pEXZ8718gaUF1i-KXIHXpdg="

    SECRET_KEY: str = "super-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 5
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 480

    RMQ_AMQP_URL: str = "amqp://guest:guest@localhost/"


settings = Settings()
