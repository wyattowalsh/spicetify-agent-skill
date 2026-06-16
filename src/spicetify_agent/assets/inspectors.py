"""Local and staged asset inspection helpers."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import Any

from ..errors import PolicyBlocked
from .path_guard import reject_symlink_components, resolve_asset_target

SECRET_MARKERS = {".env", ".ssh", "id_rsa", "id_ed25519"}


def inspect_asset_path(
    path: Path, *, asset_roots: Sequence[str | Path] | None = None
) -> dict[str, Any]:
    path = resolve_asset_target(path, roots=asset_roots)
    if any(part.lower() in SECRET_MARKERS for part in path.parts):
        raise PolicyBlocked("Refusing to inspect secret-like paths")
    if path.is_dir():
        root = path.resolve()
        children = list(path.iterdir())
        for child in children:
            reject_symlink_components(root, child)
            if any(part.lower() in SECRET_MARKERS for part in child.parts):
                raise PolicyBlocked("Refusing to inspect secret-like paths")
        names = {child.name for child in children}
        return _inspect_names(names, source=str(path))
    if not path.is_file():
        raise PolicyBlocked("Asset inspection target must be a file or directory")
    return _inspect_names({path.name}, source=str(path))


def _inspect_names(names: set[str], *, source: str) -> dict[str, Any]:
    lowered = {name.lower() for name in names}
    if {"color.ini", "user.css"} <= lowered:
        kind = "theme"
    elif "manifest.json" in lowered and "index.js" in lowered:
        kind = "custom-app"
    elif any(name.endswith((".js", ".mjs")) for name in lowered):
        kind = "extension"
    elif any(name.endswith((".css", ".scss")) for name in lowered):
        kind = "snippet"
    else:
        kind = "unknown"
    return {
        "source": source,
        "assetKind": kind,
        "files": sorted(names),
        "findings": _findings_for_names(lowered, kind),
    }


def _findings_for_names(names: set[str], kind: str) -> list[str]:
    findings: list[str] = []
    if kind == "custom-app" and "subfiles_extension" in " ".join(names):
        findings.append("custom app startup extension files require JS audit")
    if kind == "theme" and "theme.js" in names:
        findings.append("theme.js is executable JavaScript and requires audit")
    if kind == "unknown":
        findings.append("asset kind unknown until more files are provided")
    return findings
