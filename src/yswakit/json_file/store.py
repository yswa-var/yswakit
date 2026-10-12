"""Read, write, and update JSON object files."""

import json
import os
from collections.abc import Mapping
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any

from .reader import JsonFileReader


class JsonFileStore(JsonFileReader):
    """Manage JSON object files with atomic writes."""

    def __init__(
        self,
        encoding: str = "utf-8",
        *,
        indent: int | None = 2,
        sort_keys: bool = False,
    ) -> None:
        """Create a JSON store with reusable output formatting."""

        super().__init__(encoding=encoding)
        self._indent = indent
        self._sort_keys = sort_keys

    def write(
        self,
        file_path: str | Path,
        data: Mapping[str, Any],
    ) -> dict[str, Any]:
        """Atomically replace a file with a JSON object and return the saved data.

        The destination is left unchanged if JSON serialization fails.
        """

        path = Path(file_path)
        if path.is_dir():
            raise IsADirectoryError(path)

        saved_data = dict(data)
        temporary_path: Path | None = None

        try:
            with NamedTemporaryFile(
                mode="w",
                encoding=self._encoding,
                dir=path.parent,
                prefix=f".{path.name}.",
                suffix=".tmp",
                delete=False,
            ) as temporary_file:
                temporary_path = Path(temporary_file.name)
                json.dump(
                    saved_data,
                    temporary_file,
                    ensure_ascii=False,
                    indent=self._indent,
                    sort_keys=self._sort_keys,
                )
                temporary_file.write("\n")
                temporary_file.flush()
                os.fsync(temporary_file.fileno())

            temporary_path.replace(path)
        except BaseException:
            if temporary_path is not None:
                temporary_path.unlink(missing_ok=True)
            raise

        return saved_data

    def update(
        self,
        file_path: str | Path,
        changes: Mapping[str, Any],
    ) -> dict[str, Any]:
        """Shallow-merge top-level changes into a JSON object file.

        Existing keys not included in ``changes`` are preserved. The updated
        dictionary is both saved to disk and returned.
        """

        updated_data = self.read(file_path)
        updated_data.update(changes)
        return self.write(file_path, updated_data)
