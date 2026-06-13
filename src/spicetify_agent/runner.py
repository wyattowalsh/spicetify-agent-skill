"""Central subprocess runner for Spicetify commands."""

from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path

from .commands import validate_command_invocation
from .errors import PolicyBlocked


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

    def __init__(self, *, fake_binary: str | None = None, allow_real: bool = False) -> None:
        self.fake_binary = fake_binary or os.environ.get("SPICETIFY_AGENT_FAKE_BIN")
        self.allow_real = allow_real

    def run(self, command: dict[str, object]) -> CommandResult:
        command = validate_command_invocation(command)
        program = "spicetify"
        argv = command["argv"]
        assert isinstance(argv, list)
        executable = self.fake_binary or program
        fake = self.fake_binary is not None
        if fake and not self._looks_like_fake_binary(executable):
            raise PolicyBlocked("Fake Spicetify binary must be an explicit test fixture")
        if not fake and (os.environ.get("CI") or not self.allow_real):
            raise PolicyBlocked(
                "Real Spicetify execution is disabled without explicit local opt-in"
            )
        proc = subprocess.run(  # noqa: S603 - executable is policy-gated above.
            [executable, *argv],
            shell=False,
            check=False,
            text=True,
            capture_output=True,
        )
        return CommandResult(
            command_id=str(command.get("id") or "unknown"),
            argv=[program, *argv],
            returncode=proc.returncode,
            stdout=proc.stdout,
            stderr=proc.stderr,
            fake=fake,
        )

    @staticmethod
    def _looks_like_fake_binary(path: str) -> bool:
        resolved = Path(path).expanduser()
        return resolved.name.startswith("fake_spicetify") and resolved.exists()
