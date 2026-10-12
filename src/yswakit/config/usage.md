# Environment configuration

`BaseConfig` turns `.env` values and environment variables into validated,
typed settings. Add a key by declaring one more annotated class attribute.

## Import

```python
from yswakit.config import BaseConfig
```

## Quick start

Create `.env` in the current working directory:

```dotenv
CLICKHOUSE_HOST=clickhouse.internal
CLICKHOUSE_PORT=9000
DEBUG=true
API_KEY=secret-value
```

Define and load the settings:

```python
from yswakit.config import BaseConfig


class AppConfig(BaseConfig):
    CLICKHOUSE_HOST: str = "localhost"
    CLICKHOUSE_PORT: int = 8123
    DEBUG: bool = False
    API_KEY: str  # No default makes this key required.


config = AppConfig()

print(config.CLICKHOUSE_HOST)
print(config.CLICKHOUSE_PORT)  # int, not str
```

To add another key, add another typed field to `AppConfig`. Use a default for
an optional setting or omit the default to require it.

## Loading another file

```python
config = AppConfig.from_env("config/production.env")
```

Pass `None` to ignore dotenv files and use only real environment variables,
defaults, and explicit overrides:

```python
config = AppConfig.from_env(None, API_KEY="test-key", DEBUG=True)
```

## Public API

### `BaseConfig()`

Loads `.env` from the current working directory, then validates values against
the subclass's type annotations. Explicit constructor values override operating
system environment variables, which override `.env`, which overrides defaults.

Variable names are case-sensitive. Unknown keys in `.env` are ignored, allowing
multiple configuration classes to share one file.

### `BaseConfig.from_env(env_file=".env", **overrides)`

Loads a selected dotenv file. `env_file` accepts a string, `pathlib.Path`, or
`None`. Keyword overrides have the highest priority.

### `BaseConfig.as_dict()`

Returns all validated settings as a plain dictionary.

## Errors and edge cases

- A missing field without a default raises `pydantic.ValidationError`.
- A value that cannot be converted to its declared type raises
  `pydantic.ValidationError`.
- `.env` is resolved from the current working directory; parent directories are
  not searched automatically.
- For secrets, prefer Pydantic's `SecretStr` field type to avoid accidental
  display in logs.

## Dependency

This feature requires `pydantic-settings`, which is installed with `yswakit`.
