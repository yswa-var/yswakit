"""Reusable JSON file reader."""

import json
from pathlib import Path
from typing import Any


class JsonRootTypeError(ValueError):
    """Raised when a JSON document's root value is not an object."""


class JsonFileReader:
    """Read JSON object files into Python dictionaries."""

    def __init__(self, encoding: str = "utf-8") -> None:
        """Create a reader using the given text encoding."""

        if not encoding:
            raise ValueError("encoding must not be empty")
        self._encoding = encoding

    def read(self, file_path: str | Path) -> dict[str, Any]:
        """Read a JSON file and return its root object as a dictionary.

        Args:
            file_path: Path to a JSON document whose root value is an object.

        Raises:
            FileNotFoundError: If ``file_path`` does not exist.
            IsADirectoryError: If ``file_path`` points to a directory.
            UnicodeDecodeError: If the file does not use the configured encoding.
            json.JSONDecodeError: If the file does not contain valid JSON.
            JsonRootTypeError: If the JSON root is not an object.
        """

        path = Path(file_path)
        with path.open("r", encoding=self._encoding) as json_file:
            value: Any = json.load(json_file)

        if not isinstance(value, dict):
            raise JsonRootTypeError(
                f"expected a JSON object in {path}, got {type(value).__name__}"
            )

        return value
