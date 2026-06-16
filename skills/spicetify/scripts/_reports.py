"""Operation report rendering."""

from __future__ import annotations

import json
from typing import Any

from _privacy import redact


def json_report(data: dict[str, Any]) -> str:
    return redact(json.dumps(data, indent=2, sort_keys=True), strict=True) + "\n"


def markdown_report(data: dict[str, Any]) -> str:
    lines = ["# spicetify-agent report", ""]
    lines.append(f"- mode: `{data.get('mode', 'unknown')}`")
    lines.append(f"- status: `{data.get('status', 'planned')}`")
    if data.get("planHash"):
        lines.append(f"- plan hash: `{data['planHash']}`")
    if data.get("policy"):
        policy = data["policy"]
        if isinstance(policy, dict):
            lines.append(f"- risk: `{policy.get('risk', 'unknown')}`")
            lines.append(f"- confirmation required: `{policy.get('requiresConfirmation', False)}`")
    lines.append("")
    lines.append("```json")
    lines.append(redact(json.dumps(data, indent=2, sort_keys=True), strict=True))
    lines.append("```")
    return "\n".join(lines) + "\n"
