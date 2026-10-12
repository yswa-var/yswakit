"""Read JSON files as validated dictionaries."""

from .reader import JsonFileReader, JsonRootTypeError
from .store import JsonFileStore

__all__ = ["JsonFileReader", "JsonFileStore", "JsonRootTypeError"]
