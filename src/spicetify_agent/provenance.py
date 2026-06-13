"""Provenance lock helpers."""

from __future__ import annotations

from pathlib import Path

from .state import file_hash


def lock_file(path: Path, *, source: str = "local") -> dict[str, object]:
    return {
        "source": source,
        "path": str(path),
        "sha256": file_hash(path),
        "auditRequired": True,
    }


def audit_still_valid(lock: dict[str, object], path: Path) -> bool:
    return lock.get("sha256") == file_hash(path)
