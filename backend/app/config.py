"""Application configuration using Pydantic Settings."""

import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Application
    APP_NAME: str = "Shaheen Global Cloud"
    APP_VERSION: str = "0.2.0"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:postgres@localhost:5432/shaheen",
    )
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    # Security
    API_KEY: str = os.getenv("API_KEY", "dev-api-key-change-me")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-me")

    # Infrastructure
    DAGGER_MODULE_PATH: str = os.getenv("DAGGER_MODULE_PATH", "../dagger")
    TOFU_WORKDIR: str = os.getenv("TOFU_WORKDIR", "../infrastructure/environments/production")

    # Provider Configuration
    PROVIDER_TYPE: str = os.getenv("PROVIDER_TYPE", "mock")  # mock, linode
    PROVIDER_API_TOKEN: str | None = os.getenv("PROVIDER_API_TOKEN", None)
    PROVIDER_REGION: str = os.getenv("PROVIDER_REGION", "us-east")
    
    # Linode-specific settings
    LINODE_API_TOKEN: str | None = os.getenv("LINODE_API_TOKEN", None)
    LINODE_REGION: str = os.getenv("LINODE_REGION", "us-east")
    
    # Job processing
    JOB_TIMEOUT: int = 600  # 10 minutes
    JOB_POLL_INTERVAL: int = 2
    
    # Health check
    HEALTH_CHECK_TIMEOUT: int = 300  # 5 minutes
    HEALTH_CHECK_INTERVAL: int = 5
    HEALTH_CHECK_RETRIES: int = 10
    
    # Provisioning
    PROVISIONING_TIMEOUT: int = 900  # 15 minutes
    
    def validate_provider_credentials(self) -> str | None:
        """Validate that required credentials are present.
        
        Returns:
            Error message if credentials are missing, None if valid.
        """
        if self.PROVIDER_TYPE == "mock":
            return None
        
        if self.PROVIDER_TYPE == "linode":
            if not self.LINODE_API_TOKEN:
                return "LINODE_API_TOKEN environment variable is required"
            return None
        
        return f"Unknown provider type: {self.PROVIDER_TYPE}"


@lru_cache
def get_settings() -> Settings:
    return Settings()
