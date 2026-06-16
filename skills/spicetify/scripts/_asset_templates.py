"""Generated-local asset templates."""

from __future__ import annotations

from typing import Any


def template_manifest(asset_kind: str, name: str) -> dict[str, Any]:
    safe_name = _safe_name(name)
    if asset_kind == "theme":
        files = ["color.ini", "user.css", "spicetify.asset.json"]
    elif asset_kind == "custom-app":
        files = ["index.js", "manifest.json", "style.css", "spicetify.asset.json"]
    else:
        files = [f"{safe_name}.js", "spicetify.asset.json"]
    return {
        "assetKind": asset_kind,
        "name": safe_name,
        "files": files,
        "safetyDefaults": [
            "feature-detect Spicetify APIs",
            "avoid external network by default",
            "use unique storage prefix",
            "clean up listeners on unload",
            "audit generated output before enablement",
        ],
    }


def _safe_name(name: str) -> str:
    cleaned = "".join(ch if ch.isalnum() or ch in {"-", "_"} else "-" for ch in name.lower())
    return cleaned.strip("-") or "spicetify-asset"
