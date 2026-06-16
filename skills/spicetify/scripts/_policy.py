"""Risk classification, confirmation gates, and blocked-action decisions."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import cast

from _errors import ConfirmationRequired, PolicyBlocked

BLOCKED_REGEXES: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("network downloader", re.compile(r"(?<![\w-])(?:curl|wget)(?![\w-])")),
    ("shell execution", re.compile(r"(?<![\w-])(?:bash|sh|powershell|iwr|iex)(?![\w-])")),
    ("privileged filesystem command", re.compile(r"(?<![\w-])(?:sudo|chmod|chown)(?![\w-])")),
    (
        "package-manager command",
        re.compile(r"(?<![\w-])(?:npm|pnpm)\s+(?:install|run|exec|dlx)(?![\w-])"),
    ),
    (
        "package-manager command",
        re.compile(r"(?<![\w-])yarn\s+(?:install|add|run|exec|dlx)(?![\w-])"),
    ),
    ("package-manager command", re.compile(r"(?<![\w-])npx(?![\w-])")),
    ("package-manager command", re.compile(r"(?<![\w-])pip\s+install(?![\w-])")),
    (
        "package-manager command",
        re.compile(r"(?<![\w-])(?:brew|apt|apt-get|winget|choco)\s+install(?![\w-])"),
    ),
    ("remote debugging flag", re.compile(r"remote\s*-\s*debugging")),
)
BLOCKED_OPERATORS = (
    "|",
    "&&",
    ";",
    "$(",
    "`",
)

HIGH_RISK_COMMANDS = {"restore", "enable-devtools", "watch"}


@dataclass(frozen=True)
class PolicyDecision:
    risk: str
    allowed: bool
    requires_confirmation: bool
    reason: str

    def to_dict(self) -> dict[str, object]:
        return {
            "risk": self.risk,
            "allowed": self.allowed,
            "requiresConfirmation": self.requires_confirmation,
            "reason": self.reason,
        }


def classify_prompt(text: str) -> PolicyDecision:
    lowered = _normalize_policy_text(text)
    for operator in BLOCKED_OPERATORS:
        if operator in lowered:
            return PolicyDecision("blocked", False, False, "Blocked unsafe shell operator")
    for label, pattern in BLOCKED_REGEXES:
        if pattern.search(lowered):
            return PolicyDecision("blocked", False, False, f"Blocked unsafe {label}")
    return PolicyDecision("read", True, False, "No blocked shell or installer pattern detected")


def _normalize_policy_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.casefold()).strip()


def evaluate_plan(plan: dict[str, object]) -> PolicyDecision:
    commands = plan.get("commands", [])
    if not isinstance(commands, list):
        return PolicyDecision("blocked", False, False, "Plan commands must be a list")
    mutates = bool(plan.get("mutates"))
    high = any(
        str(cast(dict[str, object], command).get("id")) in HIGH_RISK_COMMANDS
        for command in commands
        if isinstance(command, dict)
    )
    if high:
        return PolicyDecision(
            "high", True, True, "High-risk command requires explicit confirmation"
        )
    if mutates:
        return PolicyDecision("medium", True, True, "Mutation requires plan-bound confirmation")
    return PolicyDecision("read", True, False, "Read-only plan")


def require_confirmation(plan_hash: str, provided: str | None, decision: PolicyDecision) -> None:
    if not decision.allowed:
        raise PolicyBlocked(decision.reason)
    if decision.requires_confirmation and provided != plan_hash:
        raise ConfirmationRequired("Confirmation must match the current plan hash")
