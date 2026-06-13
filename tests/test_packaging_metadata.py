from __future__ import annotations

import tomllib
from pathlib import Path


def test_pyproject_uses_uv_build_and_non_shadowing_console_command() -> None:
    data = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))

    assert data["build-system"]["build-backend"] == "uv_build"
    assert data["project"]["scripts"] == {"spicetify-agent": "spicetify_agent.cli:main"}
    assert "spicetify" not in data["project"]["scripts"]


def test_runtime_package_has_no_registry_dependencies() -> None:
    data = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))

    assert data["project"]["dependencies"] == []
    assert "optional-dependencies" not in data["project"]
    assert sorted(data["dependency-groups"]["dev"]) == ["mypy", "pytest", "ruff"]
