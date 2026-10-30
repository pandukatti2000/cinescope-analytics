
from functools import lru_cache

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    # PostgreSQL configuration
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "movie_rental_db"
    db_user: str = "postgres"
    db_password: SecretStr

    # OpenAI configuration
    openai_api_key: SecretStr
    openai_model: str = "gpt-4.1-mini"

    # Application configuration
    app_name: str = "Movie Rental AI Analytics"
    app_env: str = Field(default="development")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    """Load settings once and reuse them throughout the application."""
    return Settings()
