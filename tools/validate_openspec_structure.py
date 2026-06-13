#!/usr/bin/env python3
"""Validate local OpenSpec change structure without the OpenSpec CLI."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

CHANGE = "add-spicetify-skill"
REQUIREMENT = re.compile(r"^### Requirement:\s+(.+)$", re.MULTILINE)
SCENARIO = re.compile(r"^#### Scenario:\s+(.+)$", re.MULTILINE)


def load_config_domains(config_text: str) -> set[str]:
    domains: set[str] = set()
    in_domains = False
    for line in config_text.splitlines():
        stripped = line.strip()
        if stripped == "domains:":
            in_domains = True
            continue
        if in_domains:
            if stripped.startswith("- "):
                domains.add(stripped[2:].strip().strip('"'))
                continue
            if stripped and not line.startswith(" "):
                break
    return domains


def validate_spec(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    requirements = REQUIREMENT.findall(text)
    scenarios = SCENARIO.findall(text)
    if not requirements:
        errors.append(f"{path}: missing ### Requirement headings")
    if not scenarios:
        errors.append(f"{path}: missing #### Scenario headings")
    if "## ADDED Requirements" not in text:
        errors.append(f"{path}: missing ## ADDED Requirements section")
    for line in text.splitlines():
        if line.startswith("### ") and not line.startswith("### Requirement:"):
            errors.append(f"{path}: non-conforming requirement heading: {line}")
        if line.startswith("#### ") and not line.startswith("#### Scenario:"):
            errors.append(f"{path}: non-conforming scenario heading: {line}")
    return errors


def validate(root: Path) -> dict[str, object]:
    errors: list[str] = []
    change_root = root / "openspec" / "changes" / CHANGE
    config = root / "openspec" / "config.yaml"
    required = [
        config,
        change_root / "proposal.md",
        change_root / "design.md",
        change_root / "tasks.md",
        change_root / "specs",
    ]
    for path in required:
        if not path.exists():
            errors.append(f"missing required OpenSpec path: {path.relative_to(root)}")

    configured_domains = (
        load_config_domains(config.read_text(encoding="utf-8")) if config.exists() else set()
    )
    spec_files = sorted((change_root / "specs").glob("*/spec.md"))
    spec_domains = {path.parent.name for path in spec_files}
    missing = configured_domains - spec_domains
    extra = spec_domains - configured_domains
    if missing:
        errors.append("configured domains missing spec files: " + ", ".join(sorted(missing)))
    if extra:
        errors.append("spec domains missing from config: " + ", ".join(sorted(extra)))
    for path in spec_files:
        errors.extend(validate_spec(path))

    tasks = change_root / "tasks.md"
    task_ids = (
        re.findall(
            r"TASK-[0-9]{3}-[a-z0-9]+(?:-[a-z0-9]+)*",
            tasks.read_text(encoding="utf-8"),
        )
        if tasks.exists()
        else []
    )
    if len(set(task_ids)) < 20:
        errors.append("tasks.md does not contain the expected implementation task graph")

    result = {
        "root": str(root),
        "change": CHANGE,
        "configuredDomainCount": len(configured_domains),
        "specDomainCount": len(spec_domains),
        "taskIdCount": len(set(task_ids)),
        "errors": errors,
        "valid": not errors,
    }
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    result = validate(args.root.resolve())
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
