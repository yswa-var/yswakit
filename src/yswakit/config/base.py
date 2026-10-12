"""Reusable base class for typed environment configuration."""

from pathlib import Path
from typing import Any, Self

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    """Load and validate typed settings from environment variables and `.env`."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    @classmethod
    def from_env(
        cls,
        env_file: str | Path | None = ".env",
        **overrides: Any,
    ) -> Self:
        """Create settings from a chosen dotenv file plus optional overrides.

        Pass ``None`` as ``env_file`` to disable dotenv loading. Explicit
        overrides take precedence over environment variables and dotenv values.
        """

        return cls(_env_file=env_file, **overrides)

    def as_dict(self) -> dict[str, Any]:
        """Return validated settings as a plain dictionary."""

        return self.model_dump()
