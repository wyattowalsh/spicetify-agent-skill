"""Static audit rules for third-party Spicetify assets."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import Any

from .assets.path_guard import reject_symlink_components, resolve_asset_target
from .errors import PolicyBlocked

BLOCK_RULES = {
    "token exfiltration": (("localStorage", "fetch("), ("Session.accessToken", "fetch(")),
    "eval usage": (("eval(",), ("new Function",)),
    "remote code loading": (("script", "http://"), ("import(", "http://"), ("import(", "https://")),
    "remote import": (("@import url(", "http://"), ("@import url(", "https://")),
    "package lifecycle script": (('"postinstall"',), ('"preinstall"',), ('"prepare"',)),
    "prompt injection": (("ignore previous instructions",), ("ignore all safety",)),
}
WARN_RULES = {
    "minified or source-missing bundle": ((".min.js",),),
    "unstable platform api": (("Spicetify.Platform",),),
    "localStorage without namespace review": (("localStorage",),),
    "polling loop review": (("setInterval",),),
    "remote asset": (("http://",), ("https://",)),
    "marketplace metadata is not trust": (("marketplace", "stars"), ("marketplace", "popular")),
}
AUDITABLE_SUFFIXES = {".css", ".ini", ".js", ".json", ".md", ".markdown", ".txt"}
SECRET_PATH_MARKERS = {".env", ".ssh", "id_rsa", "id_dsa", "id_ecdsa", "id_ed25519"}
MAX_AUDIT_FILES = 64
MAX_AUDIT_BYTES = 1_000_000


def audit_text(text: str, *, path: str = "<memory>") -> dict[str, object]:
    lowered = text.lower()
    findings: list[dict[str, str]] = []
    for name, alternatives in BLOCK_RULES.items():
        if any(all(p.lower() in lowered for p in patterns) for patterns in alternatives):
            findings.append({"severity": "high", "reason": name, "path": path})
    for name, alternatives in WARN_RULES.items():
        if any(all(p.lower() in lowered for p in patterns) for patterns in alternatives):
            findings.append({"severity": "medium", "reason": name, "path": path})
    verdict = (
        "block"
        if any(f["severity"] == "high" for f in findings)
        else "warn"
        if findings
        else "allow"
    )
    return {"verdict": verdict, "findings": findings}


def audit_path(path: Path, *, asset_roots: Sequence[str | Path] | None = None) -> dict[str, object]:
    path = resolve_asset_target(path, roots=asset_roots)
    lowered_parts = {part.lower() for part in path.parts}
    if lowered_parts & SECRET_PATH_MARKERS:
        raise PolicyBlocked("Refusing to audit secret-like paths")
    if path.is_dir():
        return _audit_directory(path)
    if path.suffix.lower() not in AUDITABLE_SUFFIXES:
        raise PolicyBlocked("Audit targets must be text Spicetify assets or docs")
    if not path.is_file():
        raise PolicyBlocked("Audit target must be a file")
    text = path.read_text(encoding="utf-8", errors="replace")
    return audit_text(text, path=str(path))


def _audit_directory(path: Path) -> dict[str, object]:
    findings: list[dict[str, str]] = []
    files_audited = 0
    bytes_audited = 0
    skipped: list[str] = []
    coverage_truncated = False
    root = path.resolve()
    for child in sorted(path.rglob("*")):
        reject_symlink_components(root, child)
        if child.is_dir():
            continue
        lowered_parts = {part.lower() for part in child.parts}
        if lowered_parts & SECRET_PATH_MARKERS:
            raise PolicyBlocked("Refusing to audit secret-like paths")
        if child.suffix.lower() not in AUDITABLE_SUFFIXES:
            skipped.append(str(child.relative_to(path)))
            continue
        size = child.stat().st_size
        if files_audited >= MAX_AUDIT_FILES or bytes_audited + size > MAX_AUDIT_BYTES:
            skipped.append(str(child.relative_to(path)))
            coverage_truncated = True
            continue
        report = audit_text(
            child.read_text(encoding="utf-8", errors="replace"),
            path=str(child),
        )
        report_findings = report.get("findings", [])
        if isinstance(report_findings, list):
            for finding in report_findings:
                if isinstance(finding, dict):
                    findings.append({str(key): str(value) for key, value in finding.items()})
        files_audited += 1
        bytes_audited += size
    if coverage_truncated:
        findings.append(
            {
                "severity": "medium",
                "reason": "audit coverage truncated",
                "path": str(path),
            }
        )
    verdict = _verdict(findings)
    return {
        "verdict": verdict,
        "findings": findings,
        "filesAudited": files_audited,
        "bytesAudited": bytes_audited,
        "skippedFiles": skipped,
    }


def _verdict(findings: list[dict[str, Any]]) -> str:
    if any(finding.get("severity") == "high" for finding in findings):
        return "block"
    if findings:
        return "warn"
    return "allow"
