from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment or .env file."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)

    app_host: str = Field(default="127.0.0.1", validation_alias="APP_HOST")
    app_port: int = Field(default=8000, validation_alias="APP_PORT")
    debug: bool = Field(default=False, validation_alias="DEBUG")
    log_level: str = Field(default="info", validation_alias="LOG_LEVEL")
    vector_db_url: str | None = Field(default=None, validation_alias="VECTOR_DB_URL")


settings = Settings()

__all__ = ["Settings", "settings"]
