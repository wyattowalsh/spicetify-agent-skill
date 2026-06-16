"""Mode planners for the /spicetify operator."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import Any

from _asset_inspectors import inspect_asset_path
from _asset_plans import build_asset_workflow_plan
from _asset_research import build_research_report
from _audit import audit_path, audit_text
from _commands import build_command, repair_sequence
from _intent_router import contains_cue, normalize_text, route_prompt
from _platform import detect_platform
from _policy import classify_prompt, evaluate_plan
from _util import stable_hash

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
EXPLICIT_MODE_CUES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("custom-app", ("custom app", "custom-app", "customapp")),
    ("devtools", ("devtools", "developer tools")),
    ("rollback", ("rollback", "last-known-good", "last known good")),
    ("uninstall", ("uninstall",)),
    ("snapshot", ("snapshot",)),
    ("restore", ("restore",)),
    ("config", ("config",)),
    ("profile", ("profile",)),
    ("manifest", ("manifest",)),
    ("migrate", ("migrate", "migration")),
    ("marketplace", ("marketplace",)),
    ("doctor", ("doctor", "triage")),
    ("repair", ("repair", "fix", "broke", "broken")),
    ("report", ("report",)),
    ("update", ("update", "upgrade")),
    ("watch", ("watch",)),
    ("apply", ("apply",)),
    ("audit", ("audit",)),
    ("evolve", ("evolve",)),
)


def infer_mode(text: str) -> str:
    route = route_prompt(text)
    return _mode_from_route(route)


def plan_mode(
    mode: str,
    *,
    prompt: str = "",
    target: str | None = None,
    allow_network_research: bool = False,
    asset_roots: Sequence[str | Path] | None = None,
) -> dict[str, Any]:
    mode = mode.replace("_", "-")
    route: dict[str, Any] | None = None
    if mode == "plan":
        route = route_prompt(prompt)
        mode = _mode_from_route(route)
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
        if route is not None:
            blocked_plan["route"] = _sanitize_blocked_route(route)
        blocked_plan["planHash"] = stable_hash(blocked_plan)
        return blocked_plan

    route_read_only = _route_is_read_only(route)
    commands = _commands_for_mode(mode, target, prompt)
    needs_update_choice = mode == "update" and not commands
    mutates = (not route_read_only and not needs_update_choice and mode in MUTATING_MODES) or any(
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
    if route is not None:
        plan["route"] = route
        plan["nextArtifact"] = route["nextArtifact"]
        _attach_route_artifacts(
            plan,
            route,
            prompt=prompt,
            target=target,
            allow_network_research=allow_network_research,
        )
        if route_read_only:
            _force_read_only_route(plan)
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
        plan["audit"] = audit_path(Path(target), asset_roots=asset_roots)
    if mode == "inspect" and target:
        plan["inspection"] = inspect_asset_path(Path(target), asset_roots=asset_roots)
    decision = evaluate_plan(plan)
    plan["policy"] = decision.to_dict()
    plan["planHash"] = stable_hash(plan)
    return plan


def _mode_from_route(route: dict[str, Any]) -> str:
    primary = str(route.get("primaryIntent", "inspect"))
    asset_kind = str(route.get("assetKind", "unknown"))
    prompt = normalize_text(str(route.get("prompt", "")))
    explicit = _explicit_mode_from_prompt(prompt)
    if explicit is not None and not (
        primary in {"research", "audit", "evolve"} and explicit in MUTATING_MODES
    ):
        return explicit
    if primary == "refuse":
        return "inspect"
    if primary == "evolve":
        return "evolve"
    if primary == "repair":
        return "repair"
    if primary == "debug":
        return "watch" if contains_cue(prompt, "watch") else "devtools"
    if asset_kind in {"theme", "extension", "custom-app", "snippet", "marketplace"}:
        return asset_kind
    if primary == "audit":
        return "audit"
    if primary == "install-plan":
        return "apply"
    return "inspect"


def _explicit_mode_from_prompt(prompt: str) -> str | None:
    """Preserve explicit mode words for tests/traces without making them the public UX."""

    for mode, cues in EXPLICIT_MODE_CUES:
        if any(contains_cue(prompt, cue) for cue in cues):
            return mode
    return None


def _route_is_read_only(route: dict[str, Any] | None) -> bool:
    if route is None:
        return False
    primary = str(route.get("primaryIntent", "inspect"))
    if primary in {"research", "audit", "evolve"}:
        return True
    if primary != "inspect":
        return False
    explicit = _explicit_mode_from_prompt(normalize_text(str(route.get("prompt", ""))))
    return explicit not in MUTATING_MODES


def _force_read_only_route(plan: dict[str, Any]) -> None:
    plan["mutates"] = False
    commands = plan.get("commands", [])
    if isinstance(commands, list):
        plan["commands"] = [
            command
            for command in commands
            if not (isinstance(command, dict) and command.get("mutates"))
        ]
    plan["snapshot"] = {"required": False, "excludes": ["prefs", "cookies", "logs"]}
    plan["rollback"] = {"available": False, "strategy": "none"}


def _sanitize_blocked_route(route: dict[str, Any]) -> dict[str, Any]:
    sanitized = dict(route)
    sanitized["prompt"] = "[blocked unsafe prompt omitted]"
    return sanitized


def _attach_route_artifacts(
    plan: dict[str, Any],
    route: dict[str, Any],
    *,
    prompt: str,
    target: str | None,
    allow_network_research: bool,
) -> None:
    primary = str(route.get("primaryIntent", "inspect"))
    if primary == "research":
        plan["status"] = "researched"
        plan["mutates"] = False
        plan["commands"] = []
        plan["snapshot"] = {"required": False, "excludes": ["prefs", "cookies", "logs"]}
        plan["rollback"] = {"available": False, "strategy": "none"}
        plan["research"] = build_research_report(
            prompt,
            route,
            source=target,
            allow_network=allow_network_research,
        )
    elif primary == "audit":
        plan["mutates"] = False
        plan["commands"] = []
        plan["snapshot"] = {"required": False, "excludes": ["prefs", "cookies", "logs"]}
        plan["rollback"] = {"available": False, "strategy": "none"}
        if not target:
            plan["audit"] = audit_text(prompt)
    elif primary in {"create", "install-plan", "debug"}:
        plan["workflowPlan"] = build_asset_workflow_plan(route)
    elif primary == "evolve":
        plan["mutates"] = False
        plan["commands"] = []
        plan["snapshot"] = {"required": False, "excludes": ["prefs", "cookies", "logs"]}
        plan["rollback"] = {"available": False, "strategy": "none"}


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
    if mode in {"theme", "extension", "custom-app", "snippet", "marketplace", "audit"}:
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
