from pydantic import ConfigDict, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration loaded from environment or .env file."""

    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)

    app_host: str = Field("127.0.0.1", validation_alias="APP_HOST")
    app_port: int = Field(8000, validation_alias="APP_PORT")
    debug: bool = Field(False, validation_alias="DEBUG")
    log_level: str = Field("info", validation_alias="LOG_LEVEL")
    vector_db_url: str | None = Field(None, validation_alias="VECTOR_DB_URL")


settings = Settings()

__all__ = ["Settings", "settings"]
