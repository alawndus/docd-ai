from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Application configuration loaded from environment or .env file."""

    app_host: str = Field("127.0.0.1", env="APP_HOST")
    app_port: int = Field(8000, env="APP_PORT")
    debug: bool = Field(False, env="DEBUG")
    log_level: str = Field("info", env="LOG_LEVEL")
    vector_db_url: str | None = Field(None, env="VECTOR_DB_URL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

__all__ = ["Settings", "settings"]
