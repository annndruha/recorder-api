import os
from functools import lru_cache

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    DB_DSN: str
    ROOT_PATH: str = '/' + os.getenv("APP_NAME", "")
    ADMIN_TOKEN: str

    CORS_ALLOW_ORIGINS: list[str] = ['*']
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list[str] = ['*']
    CORS_ALLOW_HEADERS: list[str] = ['*']

    model_config = ConfigDict(case_sensitive=True, env_file=".env", extra="allow")


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    return settings
