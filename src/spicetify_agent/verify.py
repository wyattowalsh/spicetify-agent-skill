"""Verification helpers."""

from __future__ import annotations

from pathlib import Path


def verify_files(paths: list[Path]) -> dict[str, object]:
    checks = [{"path": str(path), "exists": path.exists()} for path in paths]
    return {"ok": all(c["exists"] for c in checks), "checks": checks}


def verify_command_results(results: list[dict[str, object]]) -> dict[str, object]:
    checks = [{"command": r.get("command_id"), "ok": r.get("returncode") == 0} for r in results]
    return {"ok": all(c["ok"] for c in checks), "checks": checks}
