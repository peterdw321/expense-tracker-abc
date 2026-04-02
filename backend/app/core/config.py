import os
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    PROJECT_NAME: str = "Expense Tracker"
    SECRET_KEY: str = "change-this-in-production-use-openssl-random-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    CORS_ORIGINS: list[str] = ["https://*.vercel.app", "http://localhost:5173", "http://localhost:3000"]

    @property
    def DATABASE_URL(self) -> str:
        url = os.environ.get('DATABASE_URL', 'postgresql+asyncpg://postgres:postgres@localhost:5432/expense_tracker')
        if url and not url.startswith('postgresql+'):
            url = url.replace('postgresql://', 'postgresql+asyncpg://', 1)
        return url

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()