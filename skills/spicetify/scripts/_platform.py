"""Read-only platform diagnostics."""

from __future__ import annotations

import platform
from pathlib import Path


def detect_platform(root: Path | None = None) -> dict[str, object]:
    markers = []
    probe_root = root or Path.cwd()
    if (probe_root / "snap").exists():
        markers.append("snap-like")
    if (probe_root / ".nix-profile").exists():
        markers.append("nix-like")
    return {
        "system": platform.system(),
        "machine": platform.machine(),
        "markers": markers,
        "manualOnly": any(m in markers for m in {"snap-like", "nix-like"}),
    }
