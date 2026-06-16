# `/spicetify`

`/spicetify` is a dry-run-first local operator for Spicetify workflows. It exposes a compact AI Skill plus an installable Python CLI, `spicetify-agent`, that plans, audits, snapshots, applies, verifies, reports, and rolls back local Spicetify customization state without granting arbitrary shell access.

The executable is intentionally named `spicetify-agent` so it does not shadow the real `spicetify` CLI.

## Install and run

Install the portable Agent Skill into supported harnesses from this checkout:

```bash
npx skills add <repo-checkout> --skill spicetify -y -g -a antigravity claude-code codex crush cursor gemini-cli github-copilot opencode
```

Install from the public repository after release:

```bash
npx skills add github:wyattowalsh/spicetify-agent-skill --skill spicetify -y -g -a antigravity claude-code codex crush cursor gemini-cli github-copilot opencode
```

The installed skill is self-contained under `skills/spicetify/`. It does not bundle the official Spicetify CLI. Users must install upstream Spicetify separately, and agents must not run installer scripts or package-manager commands without explicit approval.

From this checkout:

```bash
PYTHONPATH=skills/spicetify/scripts python3 -m spicetify_agent --help
PYTHONPATH=skills/spicetify/scripts python3 -m spicetify_agent plan "/spicetify Spotify updated and Spicetify broke"
PYTHONPATH=skills/spicetify/scripts python3 -m spicetify_agent research "find a playlist sorting extension"
```

Local package commands:

```bash
uv run spicetify-agent --help
uvx --from . spicetify-agent --help
uv build --offline
pip install dist/*.whl
spicetify-agent --help
```

## Safety model

- All potentially mutating requests produce a dry-run plan first.
- The public skill interface is prompt-first: `/spicetify <prompt input>`.
- Existing plugin, extension, theme, custom app, snippet, and Marketplace research is read-only and never installation approval.
- Mutating plans include policy, plan hash, snapshot requirement, verification, report, and rollback metadata.
- Execution uses a central argv-only runner with `shell=False`.
- Real Spicetify execution is blocked in CI and disabled locally unless explicitly opted in.
- Tests use fake Spicetify binaries and temp roots only.
- Third-party code is staged, audited, hashed, and provenance-locked before enablement.
- Installer scripts, package-manager commands, permission changes, remote debugging, screenshots, DevTools logs, network fetches, publishing, and third-party build scripts remain approval-gated.

## Main surfaces

- `skills/spicetify/scripts/` — installed-skill Python runtime and CLI.
- `skills/spicetify/` — compact `/spicetify` Skill router and references.
- `schemas/` — JSON contracts for plans, runs, reports, policy, provenance, privacy, snapshots, docs, and fixtures.
- `openspec/changes/add-spicetify-skill/` — behavior requirements and task graph.
- `apps/docs/content/docs/` — durable documentation, generated references, workflows, modes, and validation guidance.
- `apps/docs/` — isolated Fumadocs + shadcn/ui-compatible documentation app.
- `tests/` — fake-environment, policy, command, mode, audit, privacy, snapshot, CLI, and bundle validation tests.

## Prompt-first routing

The user-facing interface is natural language:

```text
/spicetify <prompt input>
```

The runtime infers intent, asset kind, source kind, risk, confidence, and the safest next artifact. Internal modes remain useful for traces, reports, and tests, but users should not need to select them up front.

Examples:

- `/spicetify find an extension for playlist sorting` returns a read-only research report.
- `/spicetify is this GitHub theme safe?` returns an audit-oriented report.
- `/spicetify safely install this Marketplace theme` returns a source-pin/stage/audit dry-run plan that requires confirmation before mutation.
- `/spicetify make a small extension that hides podcasts` returns a generated-local scaffold plan with audit and dry-run gates.

Research existing plugins, extensions, themes, custom apps, snippets, and Marketplace items as metadata only. GitHub topics, Marketplace presence, README claims, stars, and screenshots never imply trust or install approval.

Local filesystem audit/inspect targets must be staged under an approved asset root. The helper CLI defaults relative `--target` paths to the current working directory and accepts explicit staged roots with `--asset-root`; it rejects symlinks, root escapes, secret-like names, and real Spotify/Spicetify state paths.

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
uv run --frozen ty check skills/spicetify/scripts
uv build --offline
uvx --from . spicetify-agent --help
PYTHONPATH=skills/spicetify/scripts python3 -m pytest tests
PYTHONPATH=skills/spicetify/scripts python3 -m spicetify_agent validate-schemas
python3 tools/run_skill_evals.py --suite evals/spicetify-eval-suite.json --strict
python3 tools/run_skill_evals.py --suite evals/spicetify-eval-suite.json --strict --execute-fake
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
