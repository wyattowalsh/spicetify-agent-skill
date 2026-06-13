"""Risk classification, confirmation gates, and blocked-action decisions."""

from __future__ import annotations

from dataclasses import dataclass

from .errors import ConfirmationRequired, PolicyBlocked

BLOCKED_PATTERNS = (
    "curl ",
    "wget ",
    "bash ",
    "sh ",
    "sudo ",
    "chmod ",
    "chown ",
    "npm install",
    "pnpm install",
    "yarn install",
    "pip install",
    "|",
    "&&",
    ";",
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
    lowered = text.lower()
    for pattern in BLOCKED_PATTERNS:
        if pattern in lowered:
            return PolicyDecision(
                "blocked", False, False, f"Blocked unsafe pattern: {pattern.strip()}"
            )
    return PolicyDecision("read", True, False, "No blocked shell or installer pattern detected")


def evaluate_plan(plan: dict[str, object]) -> PolicyDecision:
    commands = plan.get("commands", [])
    if not isinstance(commands, list):
        return PolicyDecision("blocked", False, False, "Plan commands must be a list")
    mutates = bool(plan.get("mutates"))
    high = any(isinstance(c, dict) and str(c.get("id")) in HIGH_RISK_COMMANDS for c in commands)
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
