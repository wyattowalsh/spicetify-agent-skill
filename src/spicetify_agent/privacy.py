"""Redaction and consent helpers."""

from __future__ import annotations

import re

TOKEN = re.compile(r"(?i)(token|secret|cookie|authorization)[=: ]+([A-Za-z0-9._~+/=-]{8,})")
HOME = re.compile(r"/Users/[^/\n]+|/home/[^/\n]+|C:\\Users\\[^\\\n]+")


def redact(text: str, *, strict: bool = True) -> str:
    text = TOKEN.sub(lambda m: f"{m.group(1)}=<redacted>", text)
    if strict:
        text = HOME.sub("<home>", text)
    return text


def shareable_report(text: str) -> dict[str, object]:
    redacted = redact(text, strict=True)
    return {"text": redacted, "redacted": redacted != text, "shareable": True}
