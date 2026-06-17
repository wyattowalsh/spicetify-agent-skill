#!/usr/bin/env python3
"""Generate the flat-module schema fallback from skill-local JSON schemas."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

SCHEMA_ROOT = Path("skills") / "spicetify" / "assets" / "schemas"
OUTPUT = Path("skills") / "spicetify" / "scripts" / "_schema_data.py"


def render_schema_data(root: Path) -> str:
    schema_root = root / SCHEMA_ROOT
    entries: list[str] = []
    for path in sorted(schema_root.glob("*.json")):
        text = path.read_text(encoding="utf-8")
        entries.append(f"    {path.name!r}: {json.dumps(text)},")
    body = "\n".join(entries)
    return (
        "# ruff: noqa: E501\n"
        "# fmt: off\n"
        '"""Bundled JSON schemas for installed /spicetify skill runtime.\n\n'
        "Generated from skills/spicetify/assets/schemas/*.json. Do not edit by hand.\n"
        '"""\n\n'
        "from __future__ import annotations\n\n"
        "SCHEMAS: dict[str, str] = {\n"
        f"{body}\n"
        "}\n"
        "# fmt: on\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    root = args.root.resolve()
    output = root / OUTPUT
    expected = render_schema_data(root)
    if args.check:
        actual = output.read_text(encoding="utf-8") if output.exists() else ""
        if actual != expected:
            raise SystemExit(
                "skills/spicetify/scripts/_schema_data.py is stale; run "
                "`python3 tools/generate_schema_data.py --root .`"
            )
    else:
        output.write_text(expected, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
