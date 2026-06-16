"""Filesystem safety helpers."""

from __future__ import annotations

from pathlib import Path

from _errors import UnsafePath


def ensure_within(root: Path, candidate: Path) -> Path:
    resolved_root = root.resolve()
    resolved_candidate = candidate.resolve()
    if resolved_root != resolved_candidate and resolved_root not in resolved_candidate.parents:
        raise UnsafePath(f"Path escapes root: {candidate}")
    return resolved_candidate


def reject_symlink(path: Path) -> None:
    if path.is_symlink():
        raise UnsafePath(f"Refusing symlink path: {path}")
