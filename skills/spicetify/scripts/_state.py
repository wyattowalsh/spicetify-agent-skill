"""Snapshot, run, and rollback state."""

from __future__ import annotations

import hashlib
import os
import shutil
import time
from pathlib import Path

from _errors import UnsafePath
from _privacy import redact
from _safe_paths import ensure_within, reject_symlink
from _util import write_json

EXCLUDED_NAMES = {"prefs", "Cookies", "cookies", "logs"}


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def snapshot_tree(source: Path, snapshot_root: Path) -> dict[str, object]:
    source = source.resolve()
    snapshot_root = snapshot_root.resolve()
    if source == snapshot_root or source in snapshot_root.parents:
        raise UnsafePath("Snapshot root must be outside the source tree")
    snapshot_id = f"snapshot-{int(time.time() * 1000)}"
    target = snapshot_root / snapshot_id
    files_manifest: list[dict[str, str]] = []
    manifest: dict[str, object] = {
        "id": snapshot_id,
        "source": redact(str(source), strict=True),
        "files": files_manifest,
    }
    target.mkdir(parents=True, exist_ok=False)
    for current, dirs, files in os.walk(source):
        current_path = Path(current)
        for name in dirs:
            reject_symlink(current_path / name)
        dirs[:] = [d for d in dirs if d not in EXCLUDED_NAMES]
        for name in files:
            if name in EXCLUDED_NAMES:
                continue
            src = current_path / name
            reject_symlink(src)
            rel = src.relative_to(source)
            dst = ensure_within(target, target / rel)
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            files_manifest.append({"path": str(rel), "sha256": file_hash(src)})
    write_json(target / "snapshot-manifest.json", manifest)
    return manifest
