from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

from tests.helpers.fake_spicetify import (
    assert_fake_only_paths,
    read_jsonl,
    write_fake_spicetify_script,
)


def test_fake_spicetify_records_argv_and_simulates_success(tmp_path: Path) -> None:
    fake_bin = write_fake_spicetify_script(tmp_path / "fake_spicetify.py")
    log_path = tmp_path / "spicetify-argv.jsonl"
    env = {**os.environ, "FAKE_SPICETIFY_LOG": str(log_path)}

    result = subprocess.run(  # noqa: S603 - controlled Python fixture invocation.
        [sys.executable, str(fake_bin), "backup", "apply"],
        check=False,
        capture_output=True,
        env=env,
        text=True,
    )

    assert result.returncode == 0
    assert "fake spicetify ok" in result.stdout
    assert read_jsonl(log_path) == [
        {"argv": ["backup", "apply"], "cwd": str(Path.cwd()), "mode": "ok"}
    ]


def test_fake_spicetify_can_simulate_failure_without_real_state(tmp_path: Path) -> None:
    fake_bin = write_fake_spicetify_script(tmp_path / "fake_spicetify.py")
    log_path = tmp_path / "spicetify-argv.jsonl"
    env = {
        **os.environ,
        "FAKE_SPICETIFY_LOG": str(log_path),
        "FAKE_SPICETIFY_MODE": "fail",
    }

    result = subprocess.run(  # noqa: S603 - controlled Python fixture invocation.
        [sys.executable, str(fake_bin), "restore"],
        check=False,
        capture_output=True,
        env=env,
        text=True,
    )

    assert result.returncode == 17
    assert "fake spicetify failure" in result.stderr
    assert read_jsonl(log_path)[0]["argv"] == ["restore"]


def test_live_path_guard_rejects_real_spotify_or_spicetify_locations(tmp_path: Path) -> None:
    fake_root = tmp_path / "fake-home"
    fake_root.mkdir()

    assert_fake_only_paths(
        [fake_root / ".config" / "spicetify", fake_root / "Spotify"],
        fake_root=fake_root,
    )

    with pytest.raises(AssertionError, match="real Spotify/Spicetify path"):
        assert_fake_only_paths([Path.home() / ".config" / "spicetify"], fake_root=fake_root)
