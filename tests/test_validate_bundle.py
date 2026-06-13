from __future__ import annotations

import json
import subprocess
import sys


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
