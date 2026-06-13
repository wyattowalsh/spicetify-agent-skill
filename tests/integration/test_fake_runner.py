from __future__ import annotations

import os
from pathlib import Path

from spicetify_agent.commands import build_command
from spicetify_agent.runner import SpicetifyRunner
from tests.helpers.fake_spicetify import read_jsonl, write_fake_spicetify_script


def test_runner_executes_only_fake_fixture_binary(tmp_path: Path) -> None:
    fake_bin = write_fake_spicetify_script(tmp_path / "fake_spicetify.py")
    log_path = tmp_path / "argv.jsonl"
    old_log = os.environ.get("FAKE_SPICETIFY_LOG")
    os.environ["FAKE_SPICETIFY_LOG"] = str(log_path)
    try:
        result = SpicetifyRunner(fake_binary=str(fake_bin)).run(build_command("version"))
    finally:
        if old_log is None:
            os.environ.pop("FAKE_SPICETIFY_LOG", None)
        else:
            os.environ["FAKE_SPICETIFY_LOG"] = old_log

    assert result.returncode == 0
    assert result.fake is True
    assert read_jsonl(log_path)[0]["argv"] == ["--version"]
