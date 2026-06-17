"""Snapshot, run, and rollback state."""

from __future__ import annotations

import hashlib
import os
import re
import shutil
import time
from pathlib import Path

from _errors import UnsafePath
from _privacy import redact
from _safe_paths import ensure_within, reject_symlink
from _util import write_json

EXCLUDED_NAMES = {"prefs", "Cookies", "cookies", "logs"}
SECRET_EXACT_NAMES = {
    ".env",
    ".env.local",
    ".envrc",
    "credentials",
    "credentials.json",
    "secrets",
    "secrets.json",
}
SECRET_NAME_RE = re.compile(
    r"(^|[._-])(token|secret|credential|authorization|session|cookie)([._-]|$)",
    re.IGNORECASE,
)
MAX_SECRET_SCAN_BYTES = 64 * 1024


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _is_secret_like_name(name: str) -> bool:
    return name in SECRET_EXACT_NAMES or bool(SECRET_NAME_RE.search(name))


def _is_secret_like_path(rel: Path) -> bool:
    return any(_is_secret_like_name(part) for part in rel.parts)


def _contains_secret_like_text(path: Path) -> bool:
    try:
        if path.stat().st_size > MAX_SECRET_SCAN_BYTES:
            return False
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    return redact(text, strict=True) != text


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
        dirs[:] = [
            d
            for d in dirs
            if d not in EXCLUDED_NAMES
            and not _is_secret_like_path((current_path / d).relative_to(source))
        ]
        for name in files:
            if name in EXCLUDED_NAMES:
                continue
            src = current_path / name
            reject_symlink(src)
            rel = src.relative_to(source)
            if _is_secret_like_path(rel) or _contains_secret_like_text(src):
                continue
            dst = ensure_within(target, target / rel)
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            files_manifest.append({"path": str(rel), "sha256": file_hash(src)})
    write_json(target / "snapshot-manifest.json", manifest)
    return manifest
