"""Redaction and consent helpers."""

from __future__ import annotations

import re

BEARER = re.compile(r"(?i)(authorization:\s*bearer\s+)([A-Za-z0-9._~+/=-]{8,})")
TOKEN = re.compile(r"(?i)(token|secret|cookie|authorization)[=: ]+([A-Za-z0-9._~+/=-]{8,})")
HOME = re.compile(r"/Users/[^/\n]+|/home/[^/\n]+|C:\\Users\\[^\\\n]+")
SPOTIFY_APP = re.compile(r"/Applications/Spotify\.app")
SYNTHETIC_EVAL_CANARY = re.compile(r"FAKE_SPICETIFY_EVAL_[A-Za-z0-9_]+")


def redact(text: str, *, strict: bool = True) -> str:
    text = SYNTHETIC_EVAL_CANARY.sub("<redacted-eval-canary>", text)
    text = BEARER.sub(lambda m: f"{m.group(1)}<redacted>", text)
    text = TOKEN.sub(lambda m: f"{m.group(1)}=<redacted>", text)
    if strict:
        text = HOME.sub("<home>", text)
        text = SPOTIFY_APP.sub("<spotify-app>", text)
    return text


def shareable_report(text: str) -> dict[str, object]:
    redacted = redact(text, strict=True)
    return {"text": redacted, "redacted": redacted != text, "shareable": True}
