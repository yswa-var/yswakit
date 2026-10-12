import os
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from pydantic import ValidationError

from yswakit.config import BaseConfig


class AppConfig(BaseConfig):
    CLICKHOUSE_HOST: str = "localhost"
    CLICKHOUSE_PORT: int = 8123
    DEBUG: bool = False
    API_KEY: str


class BaseConfigTests(unittest.TestCase):
    def test_loads_and_converts_dotenv_values(self) -> None:
        with TemporaryDirectory() as directory:
            env_file = Path(directory) / ".env"
            env_file.write_text(
                "CLICKHOUSE_HOST=db.internal\n"
                "CLICKHOUSE_PORT=9000\n"
                "DEBUG=true\n"
                "API_KEY=dotenv-secret\n"
                "UNRELATED_KEY=is-ignored\n",
                encoding="utf-8",
            )

            config = AppConfig.from_env(env_file)

        self.assertEqual(config.CLICKHOUSE_HOST, "db.internal")
        self.assertEqual(config.CLICKHOUSE_PORT, 9000)
        self.assertIs(config.DEBUG, True)
        self.assertEqual(config.API_KEY, "dotenv-secret")

    def test_environment_and_explicit_values_override_dotenv(self) -> None:
        with TemporaryDirectory() as directory:
            env_file = Path(directory) / ".env"
            env_file.write_text(
                "CLICKHOUSE_PORT=9000\nAPI_KEY=dotenv-secret\n",
                encoding="utf-8",
            )
            with patch.dict(
                os.environ,
                {"CLICKHOUSE_PORT": "9100", "API_KEY": "environment-secret"},
                clear=False,
            ):
                config = AppConfig.from_env(env_file, CLICKHOUSE_PORT=9200)

        self.assertEqual(config.CLICKHOUSE_PORT, 9200)
        self.assertEqual(config.API_KEY, "environment-secret")

    def test_missing_required_key_raises_validation_error(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValidationError):
                AppConfig.from_env(None)

    def test_as_dict_returns_validated_values(self) -> None:
        config = AppConfig.from_env(None, API_KEY="test-secret")

        self.assertEqual(
            config.as_dict(),
            {
                "CLICKHOUSE_HOST": "localhost",
                "CLICKHOUSE_PORT": 8123,
                "DEBUG": False,
                "API_KEY": "test-secret",
            },
        )


if __name__ == "__main__":
    unittest.main()
