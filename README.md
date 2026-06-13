# `/spicetify`

`/spicetify` is a dry-run-first local operator for Spicetify workflows. It exposes a compact AI Skill plus an installable Python CLI, `spicetify-agent`, that plans, audits, snapshots, applies, verifies, reports, and rolls back local Spicetify customization state without granting arbitrary shell access.

The executable is intentionally named `spicetify-agent` so it does not shadow the real `spicetify` CLI.

## Install and run

From this checkout:

```bash
PYTHONPATH=src python3 -m spicetify_agent.cli --help
PYTHONPATH=src python3 -m spicetify_agent.cli plan --mode repair "spotify updated and spicetify broke"
```

Local package commands:

```bash
uv run spicetify-agent --help
uvx --from . spicetify-agent --help
uv build --no-index
pip install dist/*.whl
spicetify-agent --help
```

## Safety model

- All potentially mutating requests produce a dry-run plan first.
- Mutating plans include policy, plan hash, snapshot requirement, verification, report, and rollback metadata.
- Execution uses a central argv-only runner with `shell=False`.
- Real Spicetify execution is blocked in CI and disabled locally unless explicitly opted in.
- Tests use fake Spicetify binaries and temp roots only.
- Third-party code is staged, audited, hashed, and provenance-locked before enablement.
- Installer scripts, package-manager commands, permission changes, remote debugging, screenshots, DevTools logs, network fetches, publishing, and third-party build scripts remain approval-gated.

## Main surfaces

- `src/spicetify_agent/` — Python runtime and CLI.
- `skills/spicetify/` — compact `/spicetify` Skill router and references.
- `schemas/` — JSON contracts for plans, runs, reports, policy, provenance, privacy, snapshots, docs, and fixtures.
- `openspec/changes/add-spicetify-skill/` — behavior requirements and task graph.
- `docs/planning/add-spicetify-skill/` — implementation context, risk matrices, workflows, modes, and validation plans.
- `apps/docs/` — isolated Fumadocs + shadcn/ui-compatible documentation app.
- `tests/` — fake-environment, policy, command, mode, audit, privacy, snapshot, CLI, and bundle validation tests.

## Validation

Safe checks that do not run real Spotify or Spicetify:

```bash
uv lock --offline
uv run --frozen spicetify-agent --help
uv run --frozen pytest
uv run --frozen pytest tests/unit
uv run --frozen pytest tests/integration
uv run --frozen ruff check .
uv run --frozen ruff format --check .
uv run --frozen mypy src
uv build --no-index
uvx --from . spicetify-agent --help
PYTHONPATH=src python3 -m pytest tests
PYTHONPATH=src python3 -m spicetify_agent.cli validate-schemas
python3 tools/validate_bundle.py --root .
python3 tools/validate_openspec_structure.py --root .
python3 -m json.tool evals/regression-prompts.json >/dev/null
python3 - <<'PY'
from pathlib import Path
import json
for p in Path('schemas').glob('*.json'):
    json.load(open(p))
print('schemas ok')
PY
```

`openspec validate add-spicetify-skill --strict` and `openspec validate --all --strict` should also run in environments where the OpenSpec CLI is installed. When that CLI is unavailable, `python3 tools/validate_openspec_structure.py --root .` provides a local structural check for the active change.

## Docs app

The docs app is intentionally isolated from the Python runtime. It may document `/spicetify` behavior and generate references from local schemas/OpenSpec files, but it must not read live local Spicetify roots, snapshots, logs, screenshots, or Spotify prefs.

Dependency installation, shadcn registry access, and docs deployment require explicit approval.
