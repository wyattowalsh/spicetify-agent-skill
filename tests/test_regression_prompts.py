from __future__ import annotations

import json
from pathlib import Path

from _modes import plan_mode

EXECUTABLE_PROMPT_IDS = {"prompt_first_block_package_manager_watch"}


def test_regression_prompts_have_unique_ids_and_expected_shape() -> None:
    data = json.loads(Path("evals/regression-prompts.json").read_text(encoding="utf-8"))
    evals = data["evals"]
    ids = [item["id"] for item in evals]

    assert len(ids) == len(set(ids))
    for item in evals:
        assert item["id"]
        assert item["prompt"]
        assert item["must_include"]
        assert item["must_not_include"]
        assert all(isinstance(token, str) and token for token in item["must_include"])
        assert all(isinstance(token, str) and token for token in item["must_not_include"])


def test_regression_prompts_cover_non_negotiable_safety_stories() -> None:
    data = json.loads(Path("evals/regression-prompts.json").read_text(encoding="utf-8"))
    by_id = {item["id"]: item for item in data["evals"]}

    assert {"arbitrary_shell_refusal", "no_live_spotify_ci", "plan_hash_drift_blocks_apply"} <= set(
        by_id
    )
    assert "fake Spicetify" in by_id["no_live_spotify_ci"]["must_include"]
    assert "no live Spotify" in by_id["no_live_spotify_ci"]["must_include"]
    assert "shell" in by_id["arbitrary_shell_refusal"]["must_not_include"]
    assert "no mutation" in by_id["confirmation_plan_hash_drift"]["must_include"]


def test_executable_regression_prompts_match_planner_output() -> None:
    data = json.loads(Path("evals/regression-prompts.json").read_text(encoding="utf-8"))

    for item in data["evals"]:
        if item["id"] not in EXECUTABLE_PROMPT_IDS:
            continue
        payload = json.dumps(
            plan_mode("plan", prompt=item["prompt"]),
            sort_keys=True,
        ).lower()
        for token in item["must_include"]:
            assert token.lower() in payload
        for token in item["must_not_include"]:
            assert token.lower() not in payload
