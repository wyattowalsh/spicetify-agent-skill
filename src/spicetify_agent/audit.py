"""Static audit rules for third-party Spicetify assets."""

from __future__ import annotations

from pathlib import Path

from .errors import PolicyBlocked

BLOCK_RULES = {
    "token exfiltration": (("localStorage", "fetch("),),
    "eval usage": (("eval(",),),
    "remote import": (("@import url(", "http://"), ("@import url(", "https://")),
    "prompt injection": (("ignore previous instructions",), ("ignore all safety",)),
}
AUDITABLE_SUFFIXES = {".css", ".ini", ".js", ".json", ".md", ".markdown", ".txt"}
SECRET_PATH_MARKERS = {".env", ".ssh", "id_rsa", "id_dsa", "id_ecdsa", "id_ed25519"}


def audit_text(text: str, *, path: str = "<memory>") -> dict[str, object]:
    lowered = text.lower()
    findings: list[dict[str, str]] = []
    for name, alternatives in BLOCK_RULES.items():
        if any(all(p.lower() in lowered for p in patterns) for patterns in alternatives):
            findings.append({"severity": "high", "reason": name, "path": path})
    verdict = "block" if any(f["severity"] == "high" for f in findings) else "allow"
    return {"verdict": verdict, "findings": findings}


def audit_path(path: Path) -> dict[str, object]:
    lowered_parts = {part.lower() for part in path.parts}
    if lowered_parts & SECRET_PATH_MARKERS:
        raise PolicyBlocked("Refusing to audit secret-like paths")
    if path.suffix.lower() not in AUDITABLE_SUFFIXES:
        raise PolicyBlocked("Audit targets must be text Spicetify assets or docs")
    if not path.is_file():
        raise PolicyBlocked("Audit target must be a file")
    text = path.read_text(encoding="utf-8", errors="replace")
    return audit_text(text, path=str(path))
