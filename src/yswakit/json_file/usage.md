# JSON file reader

`JsonFileReader` reads a JSON document whose root value is an object and
returns it as a Python dictionary.

## Import

```python
from yswakit.json_file import JsonFileReader
```

## Quick start

Given `settings.json`:

```json
{
  "host": "localhost",
  "port": 8123,
  "debug": false
}
```

Read it with:

```python
from yswakit.json_file import JsonFileReader

reader = JsonFileReader()
settings = reader.read("settings.json")

print(settings["host"])
```

`settings` is a `dict[str, Any]`. Nested JSON objects remain dictionaries and
JSON arrays remain lists.

## Public API

### `JsonFileReader(encoding="utf-8")`

Creates a reusable reader. Supply another encoding only when the input file is
not UTF-8.

### `reader.read(file_path)`

Accepts a string or `pathlib.Path` and returns the JSON root object as a
dictionary.

## Errors and edge cases

- A missing path raises `FileNotFoundError`.
- A directory path raises `IsADirectoryError`.
- Invalid JSON raises `json.JSONDecodeError`.
- A root value such as a list, string, number, boolean, or `null` raises
  `yswakit.json_file.JsonRootTypeError` because it cannot be returned as the
  requested dictionary.
- Text that does not match the configured encoding raises
  `UnicodeDecodeError`.

## Dependencies

This feature uses only the Python standard library.
