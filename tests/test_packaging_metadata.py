from __future__ import annotations

import json
import os
import subprocess
import sys
import tomllib
from pathlib import Path

import spicetify_agent
from _schema_data import SCHEMAS
from _schemas import load_schema

SCRIPT_PATH = str(Path("skills/spicetify/scripts").resolve())
SCHEMA_ROOT = Path("skills/spicetify/assets/schemas")


def test_pyproject_uses_setuptools_flat_modules_and_non_shadowing_console_command() -> None:
    data = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))

    assert data["build-system"]["build-backend"] == "setuptools.build_meta"
    assert data["project"]["scripts"] == {"spicetify-agent": "spicetify_agent:main"}
    assert "spicetify" not in data["project"]["scripts"]
    assert data["tool"]["setuptools"]["package-dir"] == {"": "skills/spicetify/scripts"}
    assert "spicetify_agent" in data["tool"]["setuptools"]["py-modules"]
    assert "_modes" in data["tool"]["setuptools"]["py-modules"]


def test_runtime_package_has_no_registry_dependencies() -> None:
    data = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))

    assert data["project"]["dependencies"] == []
    assert "optional-dependencies" not in data["project"]
    assert sorted(data["dependency-groups"]["dev"]) == ["pytest", "ruff", "ty"]


def test_release_version_metadata_is_synchronized() -> None:
    pyproject = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
    version = pyproject["project"]["version"]

    assert version == "0.1.0"
    assert spicetify_agent.__version__ == version
    assert json.loads(Path("agent-bundle.json").read_text(encoding="utf-8"))["version"] == version
    assert (
        json.loads(Path(".codex-plugin/plugin.json").read_text(encoding="utf-8"))["version"]
        == version
    )
    assert (
        json.loads(Path(".claude-plugin/plugin.json").read_text(encoding="utf-8"))["version"]
        == version
    )
    assert f'version: "{version}"' in Path("skills/spicetify/agents/openai.yaml").read_text(
        encoding="utf-8"
    )


def test_packaged_schema_data_matches_skill_local_schemas() -> None:
    schema_names = sorted(path.name for path in SCHEMA_ROOT.glob("*.json"))
    package_schema_names = sorted(SCHEMAS)

    assert not (Path.cwd() / "schemas").exists()
    assert package_schema_names == schema_names
    for name in schema_names:
        assert SCHEMAS[name] == (SCHEMA_ROOT / name).read_text(encoding="utf-8")


def test_installable_skill_payload_is_self_contained() -> None:
    skill_dir = Path("skills/spicetify")
    skill = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    required_refs = {
        "references/runtime.md",
        "references/mode-router.md",
        "references/safety-policy.md",
        "references/troubleshooting.md",
        "references/spicetify-facts.md",
        "references/examples.md",
    }

    assert "name: spicetify" in skill
    assert "description:" in skill
    assert "spicetify-agent" in skill
    assert "official Spicetify CLI" in skill
    for ref in required_refs:
        assert ref in skill
        assert (skill_dir / ref).exists()
    for path in skill_dir.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        assert "../" not in text
        assert "/Users/" not in text


def test_validate_schemas_works_outside_repo_root(tmp_path: Path) -> None:
    env = {
        **os.environ,
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONPATH": SCRIPT_PATH,
    }
    result = subprocess.run(
        [sys.executable, "-m", "spicetify_agent", "validate-schemas"],
        cwd=tmp_path,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "operation-plan.schema.json" in result.stdout


def test_schema_loader_rejects_path_like_names() -> None:
    assert load_schema("request.schema.json")["title"] == "/spicetify Request"
    for name in ("../templates/custom-app/manifest.json", "request", "/request.schema.json"):
        try:
            load_schema(name)
        except FileNotFoundError:
            pass
        else:  # pragma: no cover - assertion message carries the unsafe input.
            raise AssertionError(f"schema loader accepted path-like name: {name}")
