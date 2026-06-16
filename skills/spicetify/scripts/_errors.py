"""Structured exceptions for the spicetify-agent runtime."""

from __future__ import annotations


class SpicetifyAgentError(RuntimeError):
    """Base error with a stable machine-readable code."""

    code = "spicetify_agent_error"

    def __init__(self, message: str, *, code: str | None = None) -> None:
        super().__init__(message)
        if code is not None:
            self.code = code


class PolicyBlocked(SpicetifyAgentError):
    code = "policy_blocked"


class CommandRejected(SpicetifyAgentError):
    code = "command_rejected"


class UnsafePath(SpicetifyAgentError):
    code = "unsafe_path"


class ConfirmationRequired(SpicetifyAgentError):
    code = "confirmation_required"
