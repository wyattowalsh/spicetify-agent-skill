from __future__ import annotations

import os
import subprocess
import sys
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
    assert sorted(data["dependency-groups"]["dev"]) == ["pytest", "ruff", "ty"]


def test_packaged_schema_data_matches_root_schemas() -> None:
    root_schema_names = sorted(path.name for path in Path("schemas").glob("*.json"))
    package_schema_names = sorted(
        path.name for path in Path("src/spicetify_agent/schema_data").glob("*.json")
    )

    assert package_schema_names == root_schema_names
    for name in root_schema_names:
        assert Path("src/spicetify_agent/schema_data", name).read_text(encoding="utf-8") == Path(
            "schemas", name
        ).read_text(encoding="utf-8")


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
        "PYTHONPATH": str(Path("src").resolve()),
    }
    result = subprocess.run(
        [sys.executable, "-m", "spicetify_agent.cli", "validate-schemas"],
        cwd=tmp_path,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "operation-plan.schema.json" in result.stdout
