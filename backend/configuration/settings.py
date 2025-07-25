from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    async_main_database_url: str = "postgresql+asyncpg://postgres:2476@localhost:5432/quiz"


    # class Config:
    #     env_file = ".env"
    #     env_file_encoding = "utf-8"


settings = Settings()
