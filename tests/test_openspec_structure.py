from __future__ import annotations

import json
import subprocess
import sys


def test_local_openspec_structure_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, "tools/validate_openspec_structure.py", "--root", "."],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["valid"] is True
    assert payload["specDomainCount"] == 23
    assert payload["configuredDomainCount"] == 23
