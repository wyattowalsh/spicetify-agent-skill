from __future__ import annotations

import json
from pathlib import Path

from _errors import CommandRejected, PolicyBlocked, SpicetifyAgentError
from _reports import json_report
from _util import read_json, repo_root, stable_hash, stable_json, write_json


def test_stable_json_and_hash_are_order_independent() -> None:
    left = {"b": [3, 2, 1], "a": {"z": True}}
    right = {"a": {"z": True}, "b": [3, 2, 1]}

    assert stable_json(left) == '{"a":{"z":true},"b":[3,2,1]}'
    assert stable_hash(left) == stable_hash(right)


def test_write_json_round_trips_and_leaves_no_temp_file(tmp_path: Path) -> None:
    target = tmp_path / "nested" / "report.json"
    payload = {"status": "dry-run", "mutations": []}

    write_json(target, payload)

    assert read_json(target) == payload
    assert json.loads(target.read_text(encoding="utf-8")) == payload
    assert not target.with_suffix(".json.tmp").exists()


def test_repo_root_finds_bundle_root_from_nested_path() -> None:
    nested = Path("apps/docs/content/docs/archive/add-spicetify-skill").resolve()

    assert repo_root(nested) == Path.cwd().resolve()


def test_structured_errors_keep_stable_codes() -> None:
    base = SpicetifyAgentError("base")
    override = SpicetifyAgentError("custom", code="custom_code")

    assert base.code == "spicetify_agent_error"
    assert override.code == "custom_code"
    assert PolicyBlocked("blocked").code == "policy_blocked"
    assert CommandRejected("no").code == "command_rejected"


def test_json_report_redacts_paths_and_tokens() -> None:
    rendered = json_report(
        {
            "status": "failed",
            "stdout": "token=abcdefghijk at /Users/alice/Library/Application Support/Spotify",
        }
    )

    assert "abcdefghijk" not in rendered
    assert "/Users/alice" not in rendered
    assert "<redacted>" in rendered
    assert "<home>" in rendered
