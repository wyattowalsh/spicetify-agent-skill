"""Test-only fake Spicetify helpers.

These helpers validate the CI safety contract without invoking or discovering a
real Spicetify installation.
"""

from __future__ import annotations

import json
import stat
from collections.abc import Iterable
from pathlib import Path

REAL_SPOTIFY_MARKERS = (
    ".config/spicetify",
    ".spicetify",
    "Library/Application Support/Spotify",
    "Library/Application Support/spicetify",
    "AppData/Roaming/Spotify",
    "AppData/Roaming/spicetify",
)


def assert_fake_only_paths(paths: Iterable[Path], *, fake_root: Path) -> None:
    """Fail fast if a test tries to point at live Spotify or Spicetify state."""

    fake_root_resolved = fake_root.resolve()
    for path in paths:
        resolved = path.expanduser().resolve(strict=False)
        normalized = resolved.as_posix()
        try:
            resolved.relative_to(fake_root_resolved)
        except ValueError as exc:
            if any(marker in normalized for marker in REAL_SPOTIFY_MARKERS):
                raise AssertionError(
                    f"real Spotify/Spicetify path is not allowed: {resolved}"
                ) from exc


def write_fake_spicetify_script(path: Path) -> Path:
    """Create a Python fake binary that records argv and simulates outcomes."""

    path.write_text(
        """\
#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

log_path = os.environ.get("FAKE_SPICETIFY_LOG")
mode = os.environ.get("FAKE_SPICETIFY_MODE", "ok")
record = {
    "argv": sys.argv[1:],
    "cwd": os.getcwd(),
    "mode": mode,
}
if log_path:
    with Path(log_path).open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, sort_keys=True) + "\\n")

if "--version" in sys.argv[1:]:
    print("spicetify fake-test")
elif mode == "fail":
    print("fake spicetify failure", file=sys.stderr)
    raise SystemExit(17)
else:
    print("fake spicetify ok")
""",
        encoding="utf-8",
    )
    path.chmod(path.stat().st_mode | stat.S_IXUSR)
    return path


def read_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
