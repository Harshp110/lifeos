from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", "../../.env"),
        env_file_encoding="utf-8",
        env_prefix="LIFEOS_",
        extra="ignore",
    )

    api_name: str = "LifeOS API"
    env: Literal["development", "test", "production"] = "development"
    api_host: str = "127.0.0.1"
    api_port: int = 8000
    cors_origins: str = "http://localhost:3000"
    database_url: str = Field(
        default="postgresql+psycopg://lifeos:lifeos@localhost:5432/lifeos",
    )
    redis_url: str = "redis://localhost:6379/0"
    log_level: str = "INFO"

    @property
    def cors_origin_list(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()
