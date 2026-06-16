# PLANS.md — ExecPlan for `/spicetify`

**Path:** `docs/planning/add-spicetify-skill/PLANS.md`
**Purpose:** Self-contained, living execution plan for implementing the `/spicetify` skill.
**Status:** Safe MVP kernel implemented; deep workflow tasks remain active
**Load/use when:** A coding agent needs resumable implementation context without chat history.

## Objective

Implement `/spicetify` as a safe, transactional, OpenSpec-governed local Spicetify skill/CLI. The build must start with planning, policy, snapshots, fake fixtures, and verification before any mutating mode is implemented.

## Source of truth and read order

1. `AGENTS.md`
2. `openspec/changes/add-spicetify-skill/proposal.md`
3. `openspec/changes/add-spicetify-skill/tasks.md`
4. `openspec/changes/add-spicetify-skill/specs/`
5. `openspec/changes/add-spicetify-skill/design.md`
6. `docs/planning/add-spicetify-skill/source-refresh.md`
7. `docs/planning/add-spicetify-skill/policy-matrix.md`
8. `docs/planning/add-spicetify-skill/invariants.md`
9. `docs/planning/add-spicetify-skill/failure-recovery-catalog.md`
10. `docs/planning/add-spicetify-skill/operation-state-machine.md`
11. `docs/planning/add-spicetify-skill/codex-handoff.md`

## Constraints and non-goals

- No arbitrary shell execution.
- No real Spotify/Spicetify mutation in CI.
- No package-manager install/remove/upgrade, network fetch, permission change, launch-flag edit, DevTools enablement, publishing, or external service mutation without explicit approval.
- No secrets, tokens, cookies, or Spotify prefs contents in logs/snapshots/reports.
- Non-goal: bypass Spotify account, DRM, subscription, ad, or policy controls.

## Progress

- [x] Skill name simplified to `/spicetify`.
- [x] OpenSpec change and domains drafted.
- [x] Mode catalog covers all requested modes.
- [x] Safety/policy/snapshot/provenance/verification docs added.
- [x] Source facts refreshed and conflicts recorded.
- [x] Bundle release labels removed for in-place canonical artifact.
- [x] Desired-state manifest, privacy/redaction, scaffold-template, and automation-boundary contracts added.
- [x] Non-waivable invariants and failure recovery catalog added.
- [x] Planning bundle repo grounded with read-only probes.
- [x] Implementation repo selected and grounded with read-only probes.
- [x] Bundle artifacts promoted to repo root and `spicetify_skill_planning_bundle/` removed after validation.
- [x] Python package scaffold added for `spicetify-agent` console command.
- [x] Safety kernel implemented.
- [x] Fake Spicetify integration tests implemented.
- [x] All planned modes produce structured dry-run plans.
- [x] `manifest` mode is represented in CLI, schemas, mode docs, docs map, and generated references.
- [x] Mutating `execute-plan` requires matching confirmation plus explicit snapshot roots and returns snapshot/verification/report metadata.
- [x] Companion docs app scaffold added with local content validation and LLM routes.
- [x] Generated docs reference pipeline added for schemas, OpenSpec spec domains, and mode docs.
- [x] Final-review safety blockers fixed: execution-time command registry validation, recomputed plan hash/policy verification, fake-binary fixture guard, JSON/path redaction, ambiguous update disambiguation, and generated-artifact validation skipping.
- [x] `execute-plan` now rejects mutating plans that have no executable steps, except the explicit snapshot-only mode.

## Honest implementation boundary

This repository now has a safe, installable MVP kernel: dry-run planning,
allowlisted argv-only Spicetify commands, fake-runner execution, policy and
confirmation gates, snapshot creation, redacted reports, static audit,
provenance hashing, schema/docs validators, generated references, and an
isolated docs app. It does not yet fully implement every deep workflow described
in the OpenSpec task graph. Full profile switching, theme file generation,
rollback restoration from snapshots, extension/custom-app scaffold generation,
Marketplace install planning, and complete platform fixture matrices remain
tracked tasks. Mutating plans for those incomplete workflows must stay dry-run
only until executable steps exist.

## Surprises and discoveries

- Spicetify `update` wording is ambiguous across official pages; `/spicetify` must disambiguate intent.
- Spicetify Creator has conflicting documentation status; default scaffolds should not depend on it.
- Platform repair can require package or permission actions; those belong in manual reports, not default automation.
- Marketplace convenience does not imply code trust; install scripts remain manual/approval-gated.
- The implementation is rooted at `/Users/ww/dev/projects/spicetify-agent-skill`; the former `spicetify_skill_planning_bundle/` directory has been removed after root validation passed.
- `spicetify-agent` is the installable console command so it does not shadow the real `spicetify` binary.
- Python package metadata is in `pyproject.toml`; docs-site Node metadata is isolated under `apps/docs/`.
- A docs subagent initially triggered docs dependency artifacts before approval; those artifacts were removed, then the user explicitly approved docs dependency install/build work. `pnpm-lock.yaml` is now tracked, `node_modules/` remains local/ignored, and `.gitignore` excludes generated dependency/cache outputs.
- `uv_build` is the package build backend, allowing offline `uv build --offline` with the installed `uv` executable.
- Runtime dependencies remain empty; dev/test tools are isolated in the `dev` dependency group so `uv run pytest`, `uv run ruff`, and `uv run mypy` are reproducible without adding runtime package authority.
- On this host, `python` is unavailable but `python3` is available at `/opt/homebrew/bin/python3`; use `python3` for local bundle checks while recording literal `python` command failures.
- `openspec` is unavailable on PATH in this session, but approved `npx --package @fission-ai/openspec@1.4.1 openspec ...` strict validation passes for the active change and all changes.
- Root preflight metadata was refreshed after migration so `DESIGN.md`, `openspec/config.yaml`, and `context-map.md` no longer describe the project as an external planning bundle or TypeScript runtime.
- `pnpm --filter docs lint`, `pnpm --filter docs typecheck`, and `pnpm --filter docs build` invoke pnpm dependency state checks before script execution. After explicit approval, `pnpm install --frozen-lockfile` succeeded with tracked `onlyBuiltDependencies` for `esbuild` and `sharp`; docs lint, typecheck, build, and content validation now pass.
- A local structural OpenSpec validator now covers required change files, configured spec domains, `### Requirement:` / `#### Scenario:` headings, `## ADDED Requirements` sections, and task graph presence. The global `openspec` binary remains unavailable, but approved package-scoped OpenSpec strict validation passes through `npx`.
- Package metadata no longer includes a personal author field, and `LICENSE` uses a contributor-owned copyright holder.
- Post-commit cleanup found and fixed residual TypeScript-era handoff docs in
  `repo-structure.md`, `goal.md`, `codex-handoff.md`, and `manifest.md`; the
  planning docs now point agents at the Python package runtime and isolated
  docs workspace.
- Package audit found `validate-schemas` could return success with zero schemas
  outside the repo checkout. Root schemas remain authoritative for repo work,
  and synchronized package data under `src/spicetify_agent/schema_data/` now
  supports installed `pip`/`uvx` runs.
- Follow-up review found the public `--fake-bin` option was too easy to confuse
  with a general executable override. Fake Spicetify execution now requires
  `SPICETIFY_AGENT_ALLOW_FAKE_BIN=1` in addition to the explicit fixture path
  shape, keeping fake binaries test-only by default.

## Decision log

| Context | Decision | Rationale | Revisit trigger |
|---|---|---|---|
| Naming | Keep `/spicetify` as the only user-facing skill name. | User requested simple naming and no alternate product labels. | User requests multiple skills or plugin packaging. |
| Implementation default | Use Python for the installable `spicetify-agent` CLI/runtime. | User requested pip installability and `uvx` execution. | User requests a TypeScript runtime or plugin-only package. |
| Creator | Treat Creator as legacy compatibility only. | Upstream README deprecates it while docs still describe it. | Creator is revived or replaced by an official successor. |
| Network installs | Defer behind provenance/audit/approval gates. | Supply-chain risk is too high for the first safe cutline. | User explicitly prioritizes remote install flows after local safety kernel. |
| Update repair | Decompose repair into doctor, snapshot, backup, apply, verify. | Combined commands hide checkpoints and rollback decisions. | Spicetify introduces a stable structured repair command. |
| Plan execution | Recompute executable plan hash and policy at `execute-plan` time. | Serialized JSON is editable and cannot be trusted to carry its own confirmation, policy, mutation, snapshot, or command authority. | A signed plan format or trusted local plan store is added. |
| Docs package scripts | Keep docs dependency/build authority isolated to `apps/docs` and the workspace lockfile. | The user approved docs dependency install/build work; tracked `onlyBuiltDependencies` allows required `esbuild`/`sharp` build scripts without granting the Python operator any Node runtime authority. | New docs dependencies, registry scaffolds, package scripts, or deploy/publish actions are requested. |

## Milestones

### M1 — Safety kernel

- Tasks: TASK-010 through TASK-016.
- Expected result: schemas, command registry, fake fixtures, policy, platform detection, provenance skeleton, and path guard.
- Validation: schema parse, raw-shell rejection, fake-binary smoke tests, path traversal rejection.

### M2 — Read-only skill engine

- Tasks: TASK-020 through TASK-031.
- Expected result: inspect, doctor, static audit, report.
- Validation: healthy and broken fixtures produce expected findings with no mutations.

### M3 — Local transactional mutation

- Tasks: TASK-040 through TASK-051.
- Expected result: snapshot, config/profile, theme, apply, rollback.
- Validation: fake env apply and rollback restore exact hashes.

### M4 — Repair and developer flows

- Tasks: TASK-052 through TASK-070.
- Expected result: safe post-update repair and gated extension/custom-app/devtools/watch scaffolds.
- Validation: repair fixtures stop safely for unsupported/platform/manual cases.

### M5 — Final validation and handoff

- Tasks: TASK-090 through TASK-095.
- Expected result: OpenSpec, schemas, tests, reports, docs, and handoff align.
- Validation: all target checks pass or failures are explained with evidence.

## Risks and mitigations

| Risk | Severity | Mitigation |
|---|---|---|
| Arbitrary shell path accidentally introduced | Critical | Central runner tests assert `shell:false`, no `exec`, no string command concatenation. |
| Serialized operation plan is tampered after confirmation | Critical | `execute-plan` revalidates registry commands, recomputes canonical policy and plan hash, and requires confirmation against executable contents. |
| Fake binary option becomes arbitrary executable escape hatch | High | Fake execution requires `SPICETIFY_AGENT_ALLOW_FAKE_BIN=1` and an explicit `fake_spicetify*` fixture path; real Spicetify remains blocked without local opt-in. |
| Incomplete mutating workflow reports false success | Critical | `execute-plan` rejects mutating plans without executable steps, except explicit snapshot-only runs. |
| Real Spotify mutated in tests | Critical | Fake binary and temp roots required; live paths forbidden by CI guard. |
| Third-party JS enabled after weak audit | High | Audit verdict + provenance lock + explicit acceptance bound to hashes. |
| Repair loop worsens broken Spotify state | High | Snapshot first, checkpoint each command, stop on unsupported/platform/manual cases. |
| Logs leak tokens | High | Redaction tests; no prefs/log capture by default. |
| Platform/package misclassification | Medium | Platform fixtures and manual stop paths. |
| Schema drift | Medium | Validate all JSON and schema examples in tests. |

## Validation log

| Check | Result | Notes |
|---|---|---|
| `python tools/validate_bundle.py --root .` | failed locally, exit 127 | 2026-06-13: `python` command is not available on PATH. |
| `python3 tools/validate_bundle.py --root .` | passed | 2026-06-13: validator reported 248 files, 23 spec domains, 28 root schemas, 22 mode docs, 14 workflows, 35 evals, no errors or warnings. |
| `python -m json.tool evals/regression-prompts.json >/dev/null` | failed locally, exit 127 | 2026-06-13: `python` command is not available on PATH. |
| `python3 -m json.tool evals/regression-prompts.json >/dev/null` | passed | 2026-06-13: eval JSON parsed successfully. |
| JSON schema parse | passed with `python3` | 2026-06-13: all `schemas/*.json` parsed; output `schemas ok`. |
| `PYTHONPATH=src python3 -m pytest tests` | passed | 2026-06-13: direct host pytest run passed before dev dependency group addition; uv-managed pytest now passes 71 tests. |
| `uv run --frozen pytest` | passed | 2026-06-13: 71 tests passed across unit, integration, command policy, modes, execute-plan snapshot/hash/policy enforcement, fake Spicetify fixtures, audit, privacy, provenance, snapshots, docs references, OpenSpec structure, packaging metadata, validator, and regression prompts. |
| `uv run --frozen pytest tests/unit` | passed | 2026-06-13: 1 focused unit test passed. |
| `uv run --frozen pytest tests/integration` | passed | 2026-06-13: 1 focused fake-runner integration test passed without real Spicetify access. |
| `uv run --frozen ruff format --check .` | passed | 2026-06-13: 36 files already formatted. |
| `uv run --frozen ruff check .` | passed | 2026-06-13: all selected lint/security checks passed. |
| `uv run --frozen mypy src` | passed | 2026-06-13: no issues found in 17 source files. |
| `PYTHONPATH=src python3 -m spicetify_agent.cli --help` | passed | 2026-06-13: all planned mode commands and `execute-plan`/`validate-schemas` are exposed. |
| `PYTHONPATH=src python3 -m spicetify_agent.cli validate-schemas` | passed | 2026-06-13: all 28 root schemas loaded. |
| `python3 tools/generate_docs_references.py --root . --check` | passed | 2026-06-13: generated docs references ok, 4 pages. |
| `python3 tools/validate_openspec_structure.py --root .` | passed | 2026-06-13: local structural fallback reported 23 configured domains, 23 spec domains, 38 task IDs, and no errors. |
| `node apps/docs/scripts/validate-docs-content.mjs` | passed | 2026-06-13: strict docs validator reported 12 MDX pages ok. |
| `uv --version` | passed | 2026-06-13: `uv 0.11.17` is available. |
| `uv build --offline` | passed | 2026-06-13: built sdist and wheel with bundled `uv_build`. |
| `uv lock` | passed | 2026-06-13: resolved 14 packages including isolated dev tools; runtime dependency set remains empty. |
| `uv lock --offline` | passed | 2026-06-13: lock resolution stayed available from local cache after the dev group was added. |
| `uv lock --check` | passed | 2026-06-13: lockfile remained current. |
| `uv sync --frozen` | passed | 2026-06-13: checked 13 packages from the frozen lockfile. |
| `uv run --frozen spicetify-agent --help` | passed | 2026-06-13: built and ran local console command from lockfile. |
| `uv run --frozen spicetify-agent inspect --help` | passed | 2026-06-13: mode-specific inspect help rendered successfully. |
| `uvx --from . spicetify-agent --help` | passed | 2026-06-13: built, installed, and ran the local package command. |
| Clean venv `pip install --no-index --find-links dist spicetify-agent` | passed | 2026-06-13: installed built wheel and `spicetify-agent --help` ran from the venv. |
| `uv run --frozen python -m pytest tests` | passed | 2026-06-13: dev dependency group makes pytest available in the uv project environment. |
| `pnpm install --frozen-lockfile` | passed | 2026-06-13: after explicit user approval, tracked `onlyBuiltDependencies` allowed `esbuild` and `sharp` build scripts; install completed from `pnpm-lock.yaml`. |
| `pnpm --filter docs lint` | passed | 2026-06-13: local docs lint script reported `docs lint ok`. |
| `pnpm --filter docs typecheck` | passed | 2026-06-13: `tsc --noEmit` passed. |
| `pnpm --filter docs build` | passed | 2026-06-13: Next.js 16.2.9 production build compiled, typechecked, generated 5 static pages, and finalized route output. |
| `pnpm --filter docs validate:content` | passed | 2026-06-13: strict docs validator reported 12 MDX pages ok. |
| `python3 -m build --version` | not applicable | 2026-06-13: project now uses `uv_build`; `python -m build` remains optional external tooling and was not installed. |
| `npx --yes --package @fission-ai/openspec@1.4.1 openspec validate add-spicetify-skill --strict` | passed | 2026-06-13: OpenSpec reported `Change 'add-spicetify-skill' is valid`. |
| `npx --yes --package @fission-ai/openspec@1.4.1 openspec validate --all --strict` | passed | 2026-06-13: OpenSpec reported 1 passed, 0 failed. |
| Zip integrity | not run | No archive handoff was requested after root migration; package validation used `uv build`, local `uvx --from .`, and clean-venv wheel install instead. |

## Recovery / rollback

For implementation, every mutating task must preserve prior behavior through tests and snapshots. For this planning bundle, restore from source control or the previous archived zip if a patch introduces contradictions.

## Outcomes and retrospective

Complete after implementation by recording the actual result, validation evidence, remaining risks, and follow-up work after the MVP cutline is implemented in the target repo.

## Update rules

After each implementation session, update progress, surprises/discoveries, decision log, validation log, changed files, and unresolved questions. Essential state must be in this file, not only in chat history.

## Docs-site progress lane

- [x] Confirm target repo path and package manager before docs app work.
- [x] Implement docs shell and content source scaffold.
- [x] Add shadcn/ui-compatible local risk component.
- [x] Add curated docs for quickstart, safety, and modes.
- [x] Add docs manifest and source map for generated references.
- [x] Add deterministic generated reference pages for schemas, OpenSpec spec domains, and mode docs.
- [x] Add AI-readable routes with stable redacted content.
- [x] Run docs content validation and record evidence.

Docs-site decisions and surprises must be logged here so a new agent can resume without chat history.

## Docs-site progress

- [x] Read `DESIGN.md` and docs-site planning docs.
- [x] Confirm target repo package manager and docs-site path before implementation.
- [x] Implement TASK-070/TASK-071 scaffold with evidence.
- [x] Implement TASK-072 local component scaffold with evidence.
- [x] Implement TASK-073 LLM route/source-map scaffold with evidence.
- [x] Record docs-site validation output.

## Docs-site recovery

If docs-site setup conflicts with an existing docs framework, stop and record options rather than migrating. If package installation is needed but not approved, leave a dry-run plan and no filesystem mutation.

## Subagent coordination log

Use this section when Codex subagents or worktrees are used.

| Agent | Assigned task IDs | Write scope | Status | Validation evidence | Notes |
|---|---|---|---|---|---|
| A0 repository-preflight | TASK-001, TASK-002 | `context-map.md`, `PLANS.md` | completed by orchestrator after two stalled subagent attempts were interrupted | `python` checks failed with exit 127; equivalent `python3` bundle/eval/schema checks passed; `openspec` unavailable | Subagent infrastructure accepted spawned A0 workers, but both failed to return within the preflight window. Orchestrator used the single-agent fallback envelope and recorded evidence in planning docs. |
| T6 docs-skill team | TASK-070..073 | `skills/spicetify/**`, `apps/docs/**`, docs content | interrupted, then completed by orchestrator | `pnpm --filter docs validate:content` passed | Subagent did not return an envelope before interruption; generated dependency artifacts were removed. |
| T7 validation team | TASK-012, TASK-090 | `tests/**`, `tools/**`, `evals/**` | completed | initial 10 tests passed; final orchestrator suite now passed 71 tests | Added fake Spicetify helper, validator smoke tests, regression prompt coverage, and utility/error tests. |
| T5 runtime gap audit | runtime safety/modes review | read-only | interrupted after timeout | no envelope returned | Orchestrator completed direct safety validation and later used T8 final-review findings. |
| T6 generated docs references | `tools/generate_docs_references.py`, `apps/docs/content/docs/reference/**`, docs map | interrupted after timeout; completed by orchestrator | generated-reference check passed; docs validators passed | Partial docs edits were consolidated; duplicate stale `apps/docs/scripts/generate-references.py` was removed. |
| T8 final review | final safety red-team | read-only | completed, blockers fixed by orchestrator | initial focused review found critical/high blockers; post-fix tests and validators passed | Findings drove plan hash/policy recompute, runner registry enforcement, fake-binary guard, redaction, update disambiguation, and validator artifact skipping. |
| T8 post-fix review | final blocker recheck | read-only | interrupted parent after timeout; child reviewers A8.1/A8.2 completed | A8.1 passed focused plan hash/policy/update tests; A8.2 passed focused runner/fake-binary tests; no critical/high findings in reviewed scope | Orchestrator also relied on direct post-fix validation evidence: 71 tests, ruff, mypy, docs validators, generated-reference check, bundle validator, and approved OpenSpec validation passed. |
| docs-steward review | docs/API/skill/file-structure review | review only | attempted, interrupted after timeout | direct docs validators passed | `/docs-steward` was available as a skill source in `/Users/ww/dev/projects/agents`, but the review subagent did not return an envelope in time. |
| final closure audit | final planning/docs/artifact audit | intended read-only; touched `PLANS.md`, `context-map.md`, and `validation.md` | needs-review; edits reviewed and accepted by orchestrator | bundle validator, OpenSpec structure validator, docs content validator, artifact scan, and approved npx OpenSpec checks passed | Subagent violated its read-only assignment, but edits stayed within user-approved planning write scope and corrected stale validation/tooling status. |
| final honest-review | commit-blocking safety/docs review | read-only | blockers fixed by orchestrator | focused tests passed, full suite passed, docs typecheck/build passed | Fixed config path traversal acceptance, TypeScript build-info manifest drift, stale generated manifest validation, and cache cleanup before commit. |
| T1 skill packaging | self-contained `npx skills add --skill spicetify` payload | `skills/spicetify/**`, `README.md`, `agent-bundle.json`, plugin metadata | completed by orchestrator after subagent timeout | focused packaging/regression/runtime tests passed before manifest regeneration; full validation pending | Removed repo-escaping skill references, added runtime/troubleshooting references, documented external official Spicetify CLI, and added single-skill distribution metadata. |
| T2 runtime safety | subprocess boundary hardening | `src/spicetify_agent/runner.py`, CLI/tests | completed by orchestrator after subagent timeout | focused runtime tests passed before manifest regeneration; full validation pending | Preserved fake-binary opt-in and added runner cwd, sanitized env, timeout, and redacted captured output. |
| T3 cleanup | gitignore and ignored artifacts | `.gitignore`, ignored caches/build outputs | completed by subagent with orchestrator review | ignored artifact scan showed targeted cache/build dirs removed | Added narrow env/log/coverage ignores and cleaned `dist`, tool caches, docs `.next`, and Python `__pycache__` while preserving dependency dirs. |
| T4 validation/evals | installability validator and regression prompts | `tools/validate_bundle.py`, `evals/regression-prompts.json`, tests, generated manifest | completed | `python3 tools/validate_bundle.py --root . --write-manifest` and final `python3 tools/validate_bundle.py --root .` passed with 253 files, 23 specs, 28 schemas, 40 evals | Added skill self-containment validation, bundle/plugin metadata checks, and installed-skill regression prompts. |
| T5 final review panel | docs/spec trace, runtime honest review, simplify review | read-only | timed out; completed by orchestrator local review | direct diff review plus full validation passed; no critical/high blockers found | Review subagents were interrupted after timeout with no envelopes. Orchestrator performed local review of skill payload, distribution metadata, runner boundary, validator, and tests. |

Subagent results MUST be consolidated by the orchestrator before broad design/API changes are accepted. Record conflicts, write-scope overlap, validation failures, and stop conditions here.

## 2026-06-13 installable skill finish

- Completed self-contained `skills/spicetify/` payload for single-skill `npx skills add ... --skill spicetify` install.
- Added `agent-bundle.json`, `.codex-plugin/plugin.json`, and `.claude-plugin/plugin.json` with metadata-only skill distribution surfaces.
- Preserved `spicetify-agent` as the helper command and kept the official `spicetify` CLI external.
- Hardened runner execution with fake-fixture opt-in, approved cwd, sanitized env, timeout, and redacted captured output.
- Added installability validation and regression prompts for missing CLIs, README prompt injection, third-party exfiltration, and dry-run repair.
- Cleaned ignored build/cache artifacts after validation while leaving dependency directories intact.

Validation evidence from this finish:

| Command | Status | Notes |
|---|---|---|
| `PYTHONDONTWRITEBYTECODE=1 uv run --frozen pytest` | passed | 76 tests passed. |
| `uv run --frozen ruff format --check . && uv run --frozen ruff check . && uv run --frozen mypy src` | passed | 37 files formatted, lint clean, mypy clean over 18 source files. |
| `python3 tools/validate_bundle.py --root .` | passed | 253 files, 23 specs, 28 schemas, 40 evals, no warnings. |
| `python3 tools/validate_openspec_structure.py --root .` | passed | 23 configured domains, 23 spec domains, 38 task IDs. |
| `python3 -m json.tool evals/regression-prompts.json >/dev/null` | passed | JSON parsed. |
| `schemas/*.json` parse loop | passed | Printed `schemas ok`. |
| `uv build --offline && uvx --from . spicetify-agent --help` | passed | Built sdist/wheel and ran local package command. |
| `pnpm --filter docs lint && pnpm --filter docs typecheck && pnpm --filter docs validate:content && pnpm --filter docs build` | passed | Docs lint, typecheck, content validation, and Next.js build passed. |
| `openspec validate add-spicetify-skill --strict && openspec validate --all --strict` | not available | Direct `openspec` binary was not installed. |
| `npx --yes --package @fission-ai/openspec@1.4.1 openspec validate add-spicetify-skill --strict && npx --yes --package @fission-ai/openspec@1.4.1 openspec validate --all --strict` | passed | Change valid; 1 passed, 0 failed. |
| `npx skills add . --skill spicetify --list` | passed | Found exactly 1 skill: `spicetify`. |
| temp-HOME `npx skills add . --skill spicetify -y -g -a codex` | passed | Installed 1 copied skill into the temp HOME and cleaned the temp dirs. |

## 2026-06-16 eval-hardening review closure

- Implemented the deterministic `/spicetify` eval runner and suite as executable behavior checks rather than static prompt-output assertions.
- Added structured eval schemas, packaged schema copies, fixture-backed mode coverage, result/report contracts, and local-only fake Spicetify execution.
- Added `evolve` eval coverage and installed-skill eval runbook references.
- Used read-only review subagents for honest review, simplify review, and security red-team review. Their high/medium findings were fixed before acceptance.
- Fixed review-discovered false positives: strict selected fake-exec cases now fail if all selected cases skip; fake Spicetify argv is fail-closed when not fixture-modeled; synthetic canaries and Spotify app paths are redacted; state snapshots hash file contents; real-path canaries cover Linux, macOS, and Windows; manifest `file_count` now matches emitted entries.
- Added regression tests for strict-skip failure, missing fake responses, standalone synthetic canary redaction, real-path canary collection, same-size content rewrites, fake-bin root binding, schema-required `traceOracle`, safety forbid constants, and fake-exec schema binding.
- Cleaned ignored validation caches after the final pass; dependency directories were left intact.

Subagent review closure:

| Agent | Status | Key findings | Resolution |
|---|---|---|---|
| `eval_contract_review` | completed | Schema/result/suite gaps, fixture refs not loaded, trace oracle mismatch | Fixed with structured schemas, parser checks, suite migration, fixture loader, and result contract tests. |
| `eval_safety_review` | completed | Fake execution could be static, env/fake-bin gaps, missing fixture use | Fixed with fixture materialization, fail-closed fake responses, sanitized/root-bound fake execution, and execute-fake gates. |
| `docs_skill_review` | completed | Installed payload eval reference and docs validation gaps | Added skill-local eval reference and regenerated docs/schema references. |
| `final_honest_review` | completed with blockers | Strict skipped case success, unknown fake argv success, canary leak, schema drift, manifest count | All blockers fixed and covered by regression tests. |
| `final_simplify_review` | completed with blockers | Size-only snapshots, over-escaped real-path regex, schema/runner drift | Fixed with SHA-256 snapshots, regex/canary coverage, and schema-required `traceOracle`. |
| `final_security_red_team` | completed; final follow-up passed | Strict skipped case success, synthetic canary leak, fake argv fallback, broad fake-bin gate | Fixed with strict all-skipped failure, canary/app-path redaction, fake fail-closed fallback, and mandatory fake-bin root binding. |

Final validation evidence from this pass:

| Command | Status | Notes |
|---|---|---|
| `PYTHONDONTWRITEBYTECODE=1 uv run --frozen pytest` | passed | 101 tests passed. |
| `uv run --frozen ruff format --check . && uv run --frozen ruff check . && uv run --frozen mypy src` | passed | 41 files formatted, lint clean, mypy clean over 18 source files. |
| `python3 tools/run_skill_evals.py --suite evals/spicetify-eval-suite.json --strict` | passed | 46/51 passed, 5 fake-exec-only cases skipped, 0 failed. |
| `python3 tools/run_skill_evals.py --suite evals/spicetify-eval-suite.json --strict --execute-fake --json` | passed | JSON parsed; 51/51 passed. |
| `python3 tools/run_skill_evals.py --suite evals/spicetify-eval-suite.json --mode evolve --strict --json` | passed | JSON parsed; evolve cases passed. |
| `python3 tools/run_skill_evals.py --suite evals/spicetify-eval-suite.json --category security --repeat 3 --strict --json` | passed | JSON parsed; security category repeat run passed. |
| `python3 tools/validate_bundle.py --root . --write-manifest && python3 tools/validate_bundle.py --root .` | passed | Manifest regenerated; validator reported 283 files, 23 specs, 33 schemas, 45 evals. |
| `python3 tools/validate_openspec_structure.py --root .` | passed | 23 configured domains, 23 spec domains, 38 task IDs. |
| `python3 -m json.tool evals/regression-prompts.json >/dev/null` | passed | JSON parsed. |
| `schemas/*.json` parse loop | passed | Printed `schemas ok`. |
| `npx --yes --package @fission-ai/openspec@1.4.1 openspec validate add-spicetify-skill --strict && npx --yes --package @fission-ai/openspec@1.4.1 openspec validate --all --strict` | passed | Change valid; all strict validation passed. |
| `uvx --from . spicetify-agent --help` | passed | Local package command exposed `evolve` and all modes. |
| `npx skills add . --skill spicetify --list` | passed | Found exactly one public skill: `spicetify`. |
| temp-HOME `npx skills add . --skill spicetify -y -g -a codex` | passed | Installed one copied skill into the temporary HOME. |
| `pnpm --filter docs lint && pnpm --filter docs typecheck && pnpm --filter docs validate:content && pnpm --filter docs build` | passed | Docs lint, typecheck, content validation, and Next.js build passed. |
