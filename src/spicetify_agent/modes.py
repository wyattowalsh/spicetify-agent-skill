"""Mode planners for the /spicetify operator."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .audit import audit_path, audit_text
from .commands import build_command, repair_sequence
from .platform import detect_platform
from .policy import classify_prompt, evaluate_plan
from .util import stable_hash

READ_MODES = {
    "inspect",
    "doctor",
    "audit",
    "report",
    "marketplace",
    "migrate",
    "manifest",
    "evolve",
}
MUTATING_MODES = {
    "apply",
    "config",
    "profile",
    "theme",
    "extension",
    "custom-app",
    "snippet",
    "snapshot",
    "restore",
    "rollback",
    "repair",
    "uninstall",
    "devtools",
    "watch",
    "update",
}
ALL_MODES = tuple(sorted(READ_MODES | MUTATING_MODES | {"plan"}))


def infer_mode(text: str) -> str:
    lowered = text.lower()
    if "custom app" in lowered or "custom-app" in lowered:
        return "custom-app"
    if "broke" in lowered or "broken" in lowered:
        return "repair"
    if "uninstall" in lowered or "remove" in lowered:
        return "uninstall"
    if "watch" in lowered:
        return "watch"
    for mode in ALL_MODES:
        if mode in lowered:
            return mode
    if "improve" in lowered or "optimize" in lowered or "eval" in lowered:
        return "evolve"
    if "safe" in lowered or "audit" in lowered:
        return "audit"
    return "inspect"


def plan_mode(mode: str, *, prompt: str = "", target: str | None = None) -> dict[str, Any]:
    mode = mode.replace("_", "-")
    if mode == "plan":
        mode = infer_mode(prompt)
    if mode not in ALL_MODES:
        raise ValueError(f"Unsupported mode: {mode}")
    prompt_decision = classify_prompt(prompt)
    if not prompt_decision.allowed:
        blocked_plan = {
            "mode": mode,
            "status": "blocked",
            "mutates": False,
            "commands": [],
            "policy": prompt_decision.to_dict(),
            "reason": prompt_decision.reason,
        }
        blocked_plan["planHash"] = stable_hash(blocked_plan)
        return blocked_plan

    commands = _commands_for_mode(mode, target, prompt)
    needs_update_choice = mode == "update" and not commands
    mutates = (not needs_update_choice and mode in MUTATING_MODES) or any(
        bool(c.get("mutates")) for c in commands
    )
    plan: dict[str, Any] = {
        "mode": mode,
        "status": "needs-clarification" if needs_update_choice else "planned",
        "dryRun": True,
        "mutates": mutates,
        "commands": commands,
        "preconditions": _preconditions_for_mode(mode),
        "snapshot": _snapshot_for_mode(mode),
        "verification": _verification_for_mode(mode),
        "rollback": _rollback_for_mode(mode),
        "platform": detect_platform(),
    }
    if mode == "evolve":
        plan["evolution"] = {
            "inputs": [
                "eval-results/*.json",
                "eval-traces/*.jsonl",
                "operation reports",
                "review reports",
                "user-supplied redacted transcripts",
            ],
            "output": "evolution-report",
            "rules": [
                "add or update a failing eval before behavior changes",
                "do not reduce protections to improve pass rate",
                "do not self-approve, commit, publish, install packages, or run hosted evals",
            ],
        }
    if needs_update_choice:
        plan["snapshot"] = {"required": False, "excludes": ["prefs", "cookies", "logs"]}
        plan["reason"] = (
            "Update requests must choose theme hot reload, post-Spotify repair, "
            "or manual Spicetify CLI maintenance."
        )
    if mode == "audit" and target:
        path = Path(target)
        plan["audit"] = (
            audit_path(path) if path.exists() else audit_text(prompt or target, path=target)
        )
    decision = evaluate_plan(plan)
    plan["policy"] = decision.to_dict()
    plan["planHash"] = stable_hash(plan)
    return plan


def _commands_for_mode(mode: str, target: str | None, prompt: str = "") -> list[dict[str, object]]:
    if mode == "inspect":
        return [build_command("version"), build_command("config-path"), build_command("path")]
    if mode == "doctor":
        return [build_command("version"), build_command("config-path"), build_command("path")]
    if mode == "repair":
        return repair_sequence()
    if mode == "restore":
        return [build_command("restore")]
    if mode == "apply":
        return [build_command("apply")]
    if mode == "update" and _explicit_hot_reload(target, prompt):
        return [build_command("update")]
    if mode == "watch":
        return [build_command("watch")]
    if mode == "devtools":
        return [build_command("enable-devtools")]
    if mode == "config" and target and "=" in target:
        key, value = target.split("=", 1)
        return [build_command("config", [key, value])]
    return []


def _explicit_hot_reload(target: str | None, prompt: str) -> bool:
    text = f"{target or ''} {prompt}".lower()
    return any(
        marker in text
        for marker in (
            "hot reload",
            "hot-reload",
            "reload theme",
            "current theme",
            "theme reload",
        )
    )


def _preconditions_for_mode(mode: str) -> list[str]:
    base = ["discover Spicetify config path", "confirm target paths stay inside allowed roots"]
    if mode in {"extension", "custom-app", "snippet", "marketplace", "audit"}:
        base.append("audit third-party or staged source before enablement")
    if mode in {"devtools", "watch"}:
        base.append("require bounded consent for debug session")
    return base


def _snapshot_for_mode(mode: str) -> dict[str, object]:
    required = mode in MUTATING_MODES and mode not in {"report", "audit"}
    return {"required": required, "excludes": ["prefs", "cookies", "logs"]}


def _verification_for_mode(mode: str) -> list[str]:
    checks = ["command status", "redaction check", "operation report schema"]
    if mode in MUTATING_MODES:
        checks.extend(["config/file existence", "rollback pointer"])
    if mode in {"theme", "extension", "custom-app", "snippet"}:
        checks.append("asset audit verdict")
    return checks


def _rollback_for_mode(mode: str) -> dict[str, object]:
    return {
        "available": mode in MUTATING_MODES,
        "strategy": "restore pre-mutation snapshot and verify hashes"
        if mode in MUTATING_MODES
        else "none",
    }
