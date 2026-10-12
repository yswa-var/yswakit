# JSON file reader

`JsonFileReader` reads a JSON document whose root value is an object and
returns it as a Python dictionary. `JsonFileStore` also writes and updates
JSON object files.

## Import

```python
from yswakit.json_file import JsonFileReader, JsonFileStore
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

Update selected top-level keys while preserving the others:

```python
from yswakit.json_file import JsonFileStore

store = JsonFileStore()
settings = store.update(
    "settings.json",
    {"port": 9000, "debug": True},
)

print(settings["port"])
```

Updates are shallow: replacing `{"database": {"host": "new"}}` replaces the
entire existing `database` value rather than recursively merging it.

## Public API

### `JsonFileReader(encoding="utf-8")`

Creates a reusable reader. Supply another encoding only when the input file is
not UTF-8.

### `reader.read(file_path)`

Accepts a string or `pathlib.Path` and returns the JSON root object as a
dictionary.

### `JsonFileStore(encoding="utf-8", *, indent=2, sort_keys=False)`

Creates a reader and writer. Output formatting is configured once and reused
by `write` and `update`.

### `store.write(file_path, data)`

Creates or atomically replaces a JSON object file from a mapping. Returns the
saved dictionary.

### `store.update(file_path, changes)`

Reads an existing JSON object, shallow-merges the supplied mapping, atomically
saves it, and returns the updated dictionary.

## Errors and edge cases

- A missing path raises `FileNotFoundError`.
- A directory path raises `IsADirectoryError`.
- Invalid JSON raises `json.JSONDecodeError`.
- Updating a missing file raises `FileNotFoundError`; use `write` to create it.
- Values unsupported by Python's JSON encoder raise `TypeError`. A failed
  serialization leaves an existing destination unchanged.
- A root value such as a list, string, number, boolean, or `null` raises
  `yswakit.json_file.JsonRootTypeError` because it cannot be returned as the
  requested dictionary.
- Text that does not match the configured encoding raises
  `UnicodeDecodeError`.

## Dependencies

This feature uses only the Python standard library.
