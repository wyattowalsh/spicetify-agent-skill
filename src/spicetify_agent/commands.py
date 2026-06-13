"""Allowlisted Spicetify command registry and argv builders."""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass

from .errors import CommandRejected

SAFE_VALUE = re.compile(r"^[A-Za-z0-9._@:+,\-\\/ ]{1,240}$")
SAFE_NAME = re.compile(r"^[A-Za-z0-9._@+\-]{1,120}$")


@dataclass(frozen=True)
class CommandSpec:
    name: str
    argv: tuple[str, ...]
    risk: str
    mutates: bool = False
    description: str = ""


READ_COMMANDS = {
    "version": CommandSpec("version", ("--version",), "read", False, "Read Spicetify version."),
    "config-path": CommandSpec("config-path", ("-c",), "read", False, "Read config path."),
    "path": CommandSpec("path", ("path",), "read", False, "Read known Spicetify paths."),
}

MUTATING_COMMANDS = {
    "backup": CommandSpec("backup", ("backup",), "medium", True, "Create Spicetify backup."),
    "apply": CommandSpec("apply", ("apply",), "medium", True, "Apply current config."),
    "restore": CommandSpec("restore", ("restore",), "high", True, "Restore Spotify backup."),
    "update": CommandSpec("update", ("update",), "medium", True, "Hot-reload current theme."),
    "enable-devtools": CommandSpec(
        "enable-devtools", ("enable-devtools",), "high", True, "Enable Spicetify DevTools."
    ),
    "watch": CommandSpec("watch", ("watch",), "high", True, "Start Spicetify watch mode."),
}

REGISTRY = {**READ_COMMANDS, **MUTATING_COMMANDS}


def validate_arg(value: str, *, filename: bool = False) -> str:
    pattern = SAFE_NAME if filename else SAFE_VALUE
    if not pattern.fullmatch(value):
        raise CommandRejected(f"Rejected unsafe Spicetify argument: {value!r}")
    if filename and ("/" in value or "\\" in value):
        raise CommandRejected(f"Rejected path-like filename argument: {value!r}")
    return value


def validate_config_pair(key: str, value: str) -> tuple[str, str]:
    key = validate_arg(key, filename=True)
    value = validate_arg(value)
    if "/" in value or "\\" in value or ".." in value:
        raise CommandRejected(f"Rejected path-like config value: {value!r}")
    return key, value


def build_command(command: str, values: Iterable[str] = ()) -> dict[str, object]:
    """Build a structured command invocation without shell semantics."""

    if command == "config":
        vals = list(values)
        if len(vals) != 2:
            raise CommandRejected("config command requires exactly key and value")
        key, value = validate_config_pair(vals[0], vals[1])
        argv = ("config", key, value)
        return {
            "id": "config",
            "program": "spicetify",
            "argv": list(argv),
            "risk": "medium",
            "mutates": True,
            "shell": False,
        }
    if command not in REGISTRY:
        raise CommandRejected(f"Unknown Spicetify command: {command}")
    spec = REGISTRY[command]
    extra = [validate_arg(v) for v in values]
    return {
        "id": spec.name,
        "program": "spicetify",
        "argv": [*spec.argv, *extra],
        "risk": spec.risk,
        "mutates": spec.mutates,
        "shell": False,
    }


def validate_command_invocation(command: dict[str, object]) -> dict[str, object]:
    """Re-check a serialized command immediately before execution."""

    if command.get("shell") is not False:
        raise CommandRejected("Command invocation must explicitly set shell=false")
    if command.get("program") != "spicetify":
        raise CommandRejected("Command invocation must target spicetify")
    command_id = command.get("id")
    argv = command.get("argv")
    if not isinstance(command_id, str) or not isinstance(argv, list):
        raise CommandRejected("Command invocation must include id and argv")
    if not all(isinstance(arg, str) for arg in argv):
        raise CommandRejected("Command argv must be a string array")

    if command_id == "config":
        if len(argv) != 3 or argv[0] != "config":
            raise CommandRejected("config command argv does not match registry")
        expected = build_command("config", [argv[1], argv[2]])
    else:
        if command_id not in REGISTRY:
            raise CommandRejected(f"Unknown Spicetify command: {command_id}")
        expected = build_command(command_id)
        if argv != expected["argv"]:
            raise CommandRejected(f"Command argv does not match registry for {command_id}")

    for key in ("risk", "mutates", "shell", "program", "id", "argv"):
        if command.get(key) != expected[key]:
            raise CommandRejected(f"Command field {key} does not match registry for {command_id}")
    return expected


def repair_sequence() -> list[dict[str, object]]:
    """Return checkpointed repair commands instead of combined raw commands."""

    return [build_command("backup"), build_command("apply")]
