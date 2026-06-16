from __future__ import annotations

import pytest
from _commands import build_command, validate_command_invocation
from _errors import CommandRejected


def test_registry_revalidates_serialized_commands() -> None:
    command = build_command("apply")

    assert validate_command_invocation(command)["argv"] == ["apply"]

    command["argv"] = ["restore"]
    with pytest.raises(CommandRejected):
        validate_command_invocation(command)


def test_config_command_rejects_path_like_values() -> None:
    with pytest.raises(CommandRejected):
        build_command("config", ["extensions", "../../outside.js"])

    with pytest.raises(CommandRejected):
        build_command("config", ["custom_apps", r"..\\outside"])

    assert build_command("config", ["current_theme", "Catppuccin"])["argv"] == [
        "config",
        "current_theme",
        "Catppuccin",
    ]
