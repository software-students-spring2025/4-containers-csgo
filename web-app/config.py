"""App configuration settings using pydantic for environment validation."""

import os
from typing import Any

from pydantic import PostgresDsn, computed_field, field_validator, model_validator
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings class to load environment variables and construct database URI."""

    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str | None = None
    POSTGRES_PASSWORD_FILE: str | None = None
    POSTGRES_DB: str

    @model_validator(mode="before")
    @classmethod
    def check_postgres_password(cls, data: Any) -> Any:
        """Ensure either POSTGRES_PASSWORD or POSTGRES_PASSWORD_FILE is provided."""
        if isinstance(data, dict):
            if data.get("POSTGRES_PASSWORD_FILE") is None and data.get("POSTGRES_PASSWORD") is None:
                raise ValueError("Either POSTGRES_PASSWORD or POSTGRES_PASSWORD_FILE must be set.")
        return data

    @field_validator("POSTGRES_PASSWORD_FILE", mode="before")
    @classmethod
    def read_password_from_file(cls, value: str | None) -> str | None:
        """Read password from file if file path is provided."""
        if value is not None:
            if os.path.exists(value):
                with open(value, "r", encoding="utf-8") as file:
                    return file.read().strip()
            raise ValueError(f"Password file {value} does not exist.")
        return value

    @computed_field  # type: ignore[misc]
    @property
    def sqlalchemy_database_uri(self) -> PostgresDsn:
        """Build the full SQLAlchemy URI from components."""
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD or self.POSTGRES_PASSWORD_FILE,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=f"/{self.POSTGRES_DB}",
        )


settings = Settings()
