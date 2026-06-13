# Context map

**Path:** `docs/planning/add-spicetify-skill/context-map.md`
**Purpose:** Read scope and evidence map per implementation wave.
**Status:** Current implementation evidence
**Load/use when:** Use to avoid giant prompts and hallucinated repo assumptions.


## Grounding rule

Before changing implementation behavior, refresh this file with actual evidence paths: package manager, test scripts, existing OpenSpec config, current agent instructions, relevant source directories, and validation command results.

## Current repository preflight

Checked on 2026-06-13 in `/Users/ww/dev/projects/spicetify-agent-skill`.

| Evidence | Result | Notes |
|---|---|---|
| Git root | `/Users/ww/dev/projects/spicetify-agent-skill` | `git rev-parse --show-toplevel` returned this path. |
| Implementation root | `/Users/ww/dev/projects/spicetify-agent-skill` | The former `spicetify_skill_planning_bundle/` source directory was promoted into the repo root and removed after root validation passed. |
| Root README | `README.md` documents `/spicetify`, `spicetify-agent`, safety gates, local validation, and docs-site boundaries. | Root `AGENTS.md` is present and remains the first read for this repo. |
| Git state | `main...origin/main` with uncommitted implementation files | Preserve dirty state; no branch, commit, stash, reset, stage, or push was requested. |
| Package manager | Python package uses `pyproject.toml` and `uv.lock`; docs app has isolated Node metadata under `apps/docs/`, `pnpm-lock.yaml`, and an ignored local `node_modules/` install | User approved docs dependency install/build work on 2026-06-13. Runtime dependency set remains empty, and docs Node tooling has no authority inside the Python operator. |
| Runtime package | `src/spicetify_agent/` with console command `spicetify-agent` | `/spicetify` remains the skill name; no executable named `spicetify` is created. |
| Test layout | `tests/` with fake Spicetify and temp-root coverage | CI/test behavior must not use real Spotify or Spicetify state. |
| OpenSpec config | `openspec/config.yaml` | Active change files are under `openspec/changes/add-spicetify-skill/`. |
| Local Python | `python` unavailable; `python3` available at `/opt/homebrew/bin/python3` | Literal validation commands using `python` fail with exit 127 on this host; equivalent `python3` checks pass. |
| Local OpenSpec CLI | unavailable on PATH; approved `npx --package @fission-ai/openspec@1.4.1 openspec ...` checks pass | Literal `openspec validate ...` is not installed globally, but strict validation was run through approved ephemeral npm tooling. |
| Safe validation profile | bundle validator, eval JSON parse, schema JSON parse, pytest with fake fixtures, docs content validators, docs build/typecheck/lint, uv build/install checks, OpenSpec strict validation through approved npx tooling | These checks do not execute real Spicetify, touch Spotify user state, or require package-manager mutation beyond the approved docs dependency install. |
| Write scope for current implementation | root runtime, tests, schemas, docs, OpenSpec, planning files, and package-manager lockfiles named by the approved implementation plan | Continue to avoid commits, pushes, deploys, permission changes, external service mutations, and additional dependency changes unless explicitly requested. |

## Task waves

| Wave | Tasks | Read first | Write scope | Evidence to capture |
|---|---|---|---|---|
| W0 Preflight | TASK-001..002 | `AGENTS.md`, proposal, specs, design | `context-map.md` only | repo layout, commands, package manager |
| W1 Contracts | TASK-010..012 | schemas, command workflow, validation | schemas/tests/fixtures | schema parse results, fake binary behavior |
| W2 Read-only | TASK-020..022 | skill router, inspect/doctor/audit modes | intent/modes/audit/report | prompt routing and no-mutation proof |
| W3 State/config | TASK-030..032 | state/config/profile workflows | state/config/profile modules | snapshot hash tests, config parse tests |
| W4 Mutating MVP | TASK-040..042 | apply/rollback/theme/repair workflows | core/modes/theme/repair | fake apply/rollback evidence |
| W5 Advanced | TASK-050..052 | extension/custom app/marketplace/devtools modes | scaffold/advanced modes | audit gates and confirmation tests |
| W6 Docs/reports | TASK-060..061 | UX examples, report schemas | docs/reports/examples | redaction and example consistency |
| W7 Validation | TASK-090..095 | all docs/tasks | docs/status | validation outputs |

## Source evidence already checked

| Claim | Source | Date checked | Confidence |
|---|---|---|---|
| Spicetify CLI command shapes include backup, apply, restore, update, upgrade, config, path, enable-devtools, watch, auto | Official Spicetify CLI docs | 2026-06-06 | High |
| Spicetify config is `config-xpui.ini` and CLI config editing is recommended | Official Spicetify config docs | 2026-06-06 | High |
| Themes require `color.ini` and `user.css`; home theme has priority | Official Spicetify theme docs | 2026-06-06 | High |
| Extensions/custom apps are JS assets enabled through config and apply | Official Spicetify docs | 2026-06-06 | High |
| Marketplace includes extensions, themes, snippets, and install/manage UI | Official Spicetify Marketplace docs | 2026-06-06 | High |
| Creator docs and GitHub README conflict; GitHub README says deprecated | Official docs + GitHub repo | 2026-06-06 | High |
| OpenSpec changes package proposal, design, tasks, and delta specs | OpenSpec GitHub docs | 2026-06-06 | High |

## Docs-site context map

| Task | Read first | Notes |
|---|---|---|
| TASK-070 | `DESIGN.md`, `fumadocs-site-plan.md`, `docs-site.md`, `docs-content-architecture.md`, `docs-site-design-system.md`, `docs-site-implementation-plan.md` | Confirm target repo package manager and docs path before any install or scaffold. |
| TASK-071 | `docs-content-architecture.md`, Fumadocs source docs, target package files | Content source and route work starts only after repo evidence. |
| TASK-072 | `docs-site-design-system.md`, shadcn/ui setup docs, target styling files | Registry/code copy is approval-gated and reviewable. |
| TASK-073 | `schemas/*.schema.json`, `modes/*.md`, `traceability.md`, `docs-content-architecture.md` | Generated docs must include source traceability and redaction checks. |

## Subagent swarm context map

| Agent | Read first | Evidence to capture | Write scope rule |
|---|---|---|---|
| Orchestrator | `subagent-task-graph.md`, `codex-kickoff-prompt.md`, `PLANS.md` | active task IDs, assigned write scopes, conflicts | status/planning docs only unless implementing an assigned task |
| A0 repository-preflight | repo tree, package files, OpenSpec config, AGENTS | package manager, commands, existing instructions, writable paths | context map and PLANS only |
| A1 contracts-and-schemas | `api-contracts.md`, `schemas/`, specs | schema drift and validation fixtures | schemas/schema tests only |
| A2 command-policy-state | command, policy, state specs | command allowlist, state transitions, policy decisions | core command/policy/state paths only |
| A3 audit-provenance-security | audit, provenance, privacy docs | static audit fixtures and redaction policy | audit/provenance/privacy paths only |
| A4 platform-repair-fixtures | platform matrix, recovery catalog | fake fixture coverage and platform stop rules | platform/recovery/fixture paths only |
| A5 modes-and-runtime-flows | modes and workflows | mode-controller dependency gaps | mode/router paths only after contracts stabilize |
| A6 companion-docs-site | docs-site plans and specs | docs app path, shadcn registry decisions, redaction rules | docs-site paths only |
| A7 tests-validation-evals | validation docs, evals, schemas | command results and uncovered regressions | tests/evals/validator paths only |
| A8 final-review-red-team | all changed files | cross-artifact drift and safety defects | review report only by default |
