"""Schema discovery and lightweight validation hooks."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .util import repo_root


def schema_dir() -> Path:
    return repo_root() / "schemas"


def load_schema(name: str) -> dict[str, Any]:
    path = schema_dir() / name
    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        raise ValueError(f"{name} must contain a JSON object")
    return data


def parse_all_schemas() -> list[str]:
    parsed: list[str] = []
    for path in sorted(schema_dir().glob("*.json")):
        with path.open("r", encoding="utf-8") as fh:
            json.load(fh)
        parsed.append(path.name)
    return parsed


def require_keys(data: dict[str, Any], keys: set[str], *, label: str) -> None:
    missing = sorted(keys - set(data))
    if missing:
        raise ValueError(f"{label} missing required keys: {', '.join(missing)}")
