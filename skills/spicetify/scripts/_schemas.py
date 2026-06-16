"""Schema discovery and lightweight validation hooks."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from _schema_data import SCHEMAS
from _util import repo_root


def schema_dir() -> Path | None:
    candidate = repo_root() / "schemas"
    if candidate.is_dir() and any(candidate.glob("*.json")):
        return candidate
    return None


def load_schema(name: str) -> dict[str, Any]:
    directory = schema_dir()
    if directory is not None:
        with (directory / name).open("r", encoding="utf-8") as fh:
            data = json.load(fh)
    else:
        try:
            raw = SCHEMAS[name]
        except KeyError as exc:
            raise FileNotFoundError(f"Bundled schema not found: {name}") from exc
        data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError(f"{name} must contain a JSON object")
    return data


def parse_all_schemas() -> list[str]:
    parsed: list[str] = []
    directory = schema_dir()
    if directory is not None:
        for path in sorted(directory.glob("*.json")):
            with path.open("r", encoding="utf-8") as fh:
                json.load(fh)
            parsed.append(path.name)
    else:
        for name, raw in sorted(SCHEMAS.items()):
            json.loads(raw)
            parsed.append(name)
    if not parsed:
        raise ValueError("No bundled schemas were found")
    return parsed


def require_keys(data: dict[str, Any], keys: set[str], *, label: str) -> None:
    missing = sorted(keys - set(data))
    if missing:
        raise ValueError(f"{label} missing required keys: {', '.join(missing)}")
