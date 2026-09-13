"""Application configuration using Pydantic Settings."""

import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "Shaheen Global Cloud"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:postgres@localhost:5432/shaheen",
    )
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    API_KEY: str = os.getenv("API_KEY", "dev-api-key-change-me")

    DAGGER_MODULE_PATH: str = os.getenv("DAGGER_MODULE_PATH", "../dagger")
    TOFU_WORKDIR: str = os.getenv("TOFU_WORKDIR", "../infrastructure/environments/production")

    JOB_TIMEOUT: int = 300
    JOB_POLL_INTERVAL: int = 2


@lru_cache
def get_settings() -> Settings:
    return Settings()
