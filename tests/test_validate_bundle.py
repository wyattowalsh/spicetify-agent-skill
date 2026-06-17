from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

STALE_DOCS_APP = "apps" + "/docs"


def _copy_repo_for_validator_test(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    shutil.copytree(
        Path.cwd(),
        repo,
        ignore=shutil.ignore_patterns(
            ".git",
            ".next",
            ".pytest_cache",
            ".mypy_cache",
            ".ruff_cache",
            ".venv",
            "__pycache__",
            "build",
            "dist",
            "node_modules",
        ),
    )
    return repo


def test_validate_bundle_emits_passing_json_for_current_bundle() -> None:
    result = subprocess.run(
        [sys.executable, "tools/validate_bundle.py", "--root", "."],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["valid"] is True
    assert payload["errors"] == []
    assert payload["spec_count"] >= 1
    assert payload["eval_count"] >= 1


def test_generated_manifest_is_relative_and_current() -> None:
    manifest = json.loads(open("manifest.generated.json", encoding="utf-8").read())

    assert manifest["root"] == "."
    assert manifest["file_count"] >= len(manifest["files"])
    assert all(not file["path"].startswith("/mnt/data") for file in manifest["files"])
    skipped_prefixes = (
        ".mypy_cache/",
        ".pytest_cache/",
        ".ruff_cache/",
        ".venv/",
        "docs/.next/",
        "node_modules/",
    )
    assert all(not file["path"].startswith(skipped_prefixes) for file in manifest["files"])


def test_validate_bundle_requires_release_surfaces_after_manifest_regeneration(
    tmp_path: Path,
) -> None:
    repo = _copy_repo_for_validator_test(tmp_path)
    (repo / "RELEASE.md").unlink()

    result = subprocess.run(  # noqa: S603 - test invokes this repository's validator script.
        [sys.executable, "tools/validate_bundle.py", "--root", str(repo), "--write-manifest"],
        cwd=repo,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert "missing RELEASE.md" in payload["errors"]
    assert "missing release tag surface RELEASE.md" in payload["errors"]


def test_validate_bundle_requires_root_docs_after_manifest_regeneration(tmp_path: Path) -> None:
    repo = _copy_repo_for_validator_test(tmp_path)
    shutil.rmtree(repo / "docs")

    result = subprocess.run(  # noqa: S603 - test invokes this repository's validator script.
        [sys.executable, "tools/validate_bundle.py", "--root", str(repo), "--write-manifest"],
        cwd=repo,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert "missing docs/" in payload["errors"]
    assert "missing docs/content/docs/index.mdx" in payload["errors"]


def test_validate_bundle_rejects_stale_apps_docs_after_manifest_regeneration(
    tmp_path: Path,
) -> None:
    repo = _copy_repo_for_validator_test(tmp_path)
    stale = repo / STALE_DOCS_APP
    stale.mkdir(parents=True)
    (stale / "README.md").write_text("stale docs app\n", encoding="utf-8")

    result = subprocess.run(  # noqa: S603 - test invokes this repository's validator script.
        [sys.executable, "tools/validate_bundle.py", "--root", str(repo), "--write-manifest"],
        cwd=repo,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert f"stale {STALE_DOCS_APP}/ must be moved to docs/" in payload["errors"]


def test_validate_bundle_rejects_stale_apps_docs_text_after_manifest_regeneration(
    tmp_path: Path,
) -> None:
    repo = _copy_repo_for_validator_test(tmp_path)
    readme = repo / "README.md"
    readme.write_text(
        readme.read_text(encoding="utf-8") + f"\nSee {STALE_DOCS_APP}.\n",
        encoding="utf-8",
    )

    result = subprocess.run(  # noqa: S603 - test invokes this repository's validator script.
        [sys.executable, "tools/validate_bundle.py", "--root", str(repo), "--write-manifest"],
        cwd=repo,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert f"README.md contains stale {STALE_DOCS_APP} reference" in payload["errors"]


def test_validate_bundle_rejects_root_schema_dir_after_manifest_regeneration(
    tmp_path: Path,
) -> None:
    repo = _copy_repo_for_validator_test(tmp_path)
    stale_schema_dir = repo / "schemas"
    stale_schema_dir.mkdir()
    (stale_schema_dir / "request.schema.json").write_text(
        '{"type": "object"}\n',
        encoding="utf-8",
    )

    result = subprocess.run(  # noqa: S603 - test invokes this repository's validator script.
        [sys.executable, "tools/validate_bundle.py", "--root", str(repo), "--write-manifest"],
        cwd=repo,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert "root schemas/ must be moved into skills/spicetify/assets/schemas/" in payload["errors"]


def test_validate_bundle_rejects_root_schema_text_reference_after_manifest_regeneration(
    tmp_path: Path,
) -> None:
    repo = _copy_repo_for_validator_test(tmp_path)
    readme = repo / "README.md"
    stale_schema_ref = "schemas" + "/request.schema.json"
    readme.write_text(
        readme.read_text(encoding="utf-8") + f"\nSee {stale_schema_ref}.\n",
        encoding="utf-8",
    )

    result = subprocess.run(  # noqa: S603 - test invokes this repository's validator script.
        [sys.executable, "tools/validate_bundle.py", "--root", str(repo), "--write-manifest"],
        cwd=repo,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert (
        "README.md contains stale root schema reference; use skills/spicetify/assets/schemas/"
    ) in payload["errors"]
