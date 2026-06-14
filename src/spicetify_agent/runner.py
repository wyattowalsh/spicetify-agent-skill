"""Central subprocess runner for Spicetify commands."""

from __future__ import annotations

import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

from .commands import validate_command_invocation
from .errors import PolicyBlocked

FAKE_BINARY_ENV = "SPICETIFY_AGENT_FAKE_BIN"
ALLOW_FAKE_BINARY_ENV = "SPICETIFY_AGENT_ALLOW_FAKE_BIN"
DEFAULT_TIMEOUT_SECONDS = 30

_SAFE_ENV_KEYS = {
    "APPDATA",
    "FAKE_SPICETIFY_LOG",
    "FAKE_SPICETIFY_MODE",
    "HOME",
    "LANG",
    "LC_ALL",
    "LOCALAPPDATA",
    "PATH",
    "PATHEXT",
    "SystemRoot",
    "TEMP",
    "TMP",
    "TMPDIR",
    "USERPROFILE",
    "XDG_CONFIG_HOME",
    "XDG_DATA_HOME",
}
_SENSITIVE_ENV_PARTS = ("AUTH", "COOKIE", "CREDENTIAL", "KEY", "PASS", "SECRET", "TOKEN")
_REDACTION_PATTERNS = [
    re.compile(r"(?i)(authorization:\s*bearer\s+)[^\s]+"),
    re.compile(r"(?i)(cookie:\s*)[^\r\n]+"),
    re.compile(r"(?i)((?:token|secret|password|api[_-]?key)=)([^\s&]+)"),
]


@dataclass(frozen=True)
class CommandResult:
    command_id: str
    argv: list[str]
    returncode: int
    stdout: str
    stderr: str
    fake: bool


class SpicetifyRunner:
    """Run allowlisted commands using argv arrays only."""

    def __init__(
        self,
        *,
        fake_binary: str | None = None,
        allow_real: bool = False,
        cwd: Path | None = None,
        timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
    ) -> None:
        self.fake_binary = fake_binary or os.environ.get(FAKE_BINARY_ENV)
        self.allow_real = allow_real
        self.cwd = (cwd or Path.cwd()).resolve()
        if not self.cwd.is_dir():
            raise PolicyBlocked(f"Runner cwd is not a directory: {self.cwd}")
        if timeout_seconds < 1 or timeout_seconds > 300:
            raise PolicyBlocked("Runner timeout must be between 1 and 300 seconds")
        self.timeout_seconds = timeout_seconds

    def run(self, command: dict[str, object]) -> CommandResult:
        command = validate_command_invocation(command)
        program = "spicetify"
        argv = command["argv"]
        assert isinstance(argv, list)
        executable = self.fake_binary or program
        fake = self.fake_binary is not None
        if fake and os.environ.get(ALLOW_FAKE_BINARY_ENV) != "1":
            raise PolicyBlocked("Fake Spicetify execution is only allowed for test fixtures")
        if fake and not self._looks_like_fake_binary(executable):
            raise PolicyBlocked("Fake Spicetify binary must be an explicit test fixture")
        if not fake and (os.environ.get("CI") or not self.allow_real):
            raise PolicyBlocked(
                "Real Spicetify execution is disabled without explicit local opt-in"
            )
        try:
            proc = subprocess.run(  # noqa: S603 - executable is policy-gated above.
                [executable, *argv],
                shell=False,
                check=False,
                text=True,
                capture_output=True,
                cwd=self.cwd,
                env=self._sanitized_env(),
                timeout=self.timeout_seconds,
            )
        except subprocess.TimeoutExpired as exc:
            timed_out_stdout = (
                exc.stdout.decode(errors="replace") if isinstance(exc.stdout, bytes) else exc.stdout
            )
            return CommandResult(
                command_id=str(command.get("id") or "unknown"),
                argv=[program, *argv],
                returncode=124,
                stdout=self._redact_output(timed_out_stdout or ""),
                stderr=f"Spicetify command timed out after {self.timeout_seconds} seconds",
                fake=fake,
            )
        return CommandResult(
            command_id=str(command.get("id") or "unknown"),
            argv=[program, *argv],
            returncode=proc.returncode,
            stdout=self._redact_output(proc.stdout),
            stderr=self._redact_output(proc.stderr),
            fake=fake,
        )

    @staticmethod
    def _looks_like_fake_binary(path: str) -> bool:
        resolved = Path(path).expanduser()
        return resolved.name.startswith("fake_spicetify") and resolved.exists()

    @staticmethod
    def _sanitized_env() -> dict[str, str]:
        env: dict[str, str] = {}
        for key, value in os.environ.items():
            sensitive = any(part in key.upper() for part in _SENSITIVE_ENV_PARTS)
            if key in _SAFE_ENV_KEYS and not sensitive:
                env[key] = value
        return env

    @staticmethod
    def _redact_output(text: str) -> str:
        redacted = text
        for pattern in _REDACTION_PATTERNS:
            redacted = pattern.sub(lambda match: match.group(1) + "[REDACTED]", redacted)
        home = os.environ.get("HOME")
        if home:
            redacted = redacted.replace(home, "~")
        return redacted
