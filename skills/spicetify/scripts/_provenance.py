"""Provenance lock helpers."""

from __future__ import annotations

from pathlib import Path

from _state import file_hash


def lock_file(path: Path, *, source: str = "local") -> dict[str, object]:
    return {
        "source": source,
        "sourceKind": source,
        "path": str(path),
        "sha256": file_hash(path),
        "auditRequired": True,
    }


def lock_asset_source(
    path: Path,
    *,
    source_kind: str,
    source_url: str | None = None,
    ref: str | None = None,
    audit_id: str | None = None,
    audit_verdict: str | None = None,
) -> dict[str, object]:
    """Create a provenance lock for a staged asset source."""

    return {
        "source": source_kind,
        "sourceKind": source_kind,
        "sourceUrl": source_url,
        "ref": ref,
        "path": str(path),
        "sha256": file_hash(path),
        "auditId": audit_id,
        "auditVerdict": audit_verdict,
        "auditRequired": audit_verdict != "allow",
        "trusted": False,
    }


def audit_still_valid(lock: dict[str, object], path: Path) -> bool:
    return lock.get("sha256") == file_hash(path)
