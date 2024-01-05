import tomllib
from pathlib import Path
from typing import Any


def index_or_zero(types, value):
    if value is None:
        return 0
    return types.index(value)


def load_toml_config(file: Path) -> dict[str, Any]:
    with open(file, "rb") as f:
        return tomllib.load(f)


def load_config_file(file: Path) -> dict[str, Any]:
    if file.suffix == ".toml":
        return load_toml_config(file)
    raise Exception(f"Unknown config file type: {file.suffix}")
