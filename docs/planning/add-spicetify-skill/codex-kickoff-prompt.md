# Codex kickoff prompt for the `/spicetify` swarm

**Path:** `docs/planning/add-spicetify-skill/codex-kickoff-prompt.md`
**Purpose:** Copyable kickoff prompt for Codex to implement or review `/spicetify` using bounded subagents.
**Status:** Proposed
**Load/use when:** Starting a Codex CLI/app/cloud task that should use a swarm-style task split or a sequential fallback.

## Copyable prompt

```markdown
You are Codex working on the OpenSpec change `add-spicetify-skill` for the `/spicetify` skill.

Goal: implement or review the next safe slice of `/spicetify` according to the OpenSpec artifacts and the subagent task graph. `/spicetify` is a local, dry-run-first, snapshot-protected Spicetify operator. It must never run arbitrary shell, touch real Spotify/Spicetify in CI, trust third-party code by default, or bypass confirmations.

Read first, in this order:
1. `AGENTS.md`
2. `README.md`
3. `DESIGN.md`
4. `openspec/changes/add-spicetify-skill/proposal.md`
5. `openspec/changes/add-spicetify-skill/tasks.md`
6. `openspec/changes/add-spicetify-skill/specs/`
7. `docs/planning/add-spicetify-skill/subagent-task-graph.md`
8. `docs/planning/add-spicetify-skill/context-map.md`
9. `docs/planning/add-spicetify-skill/PLANS.md`
10. `docs/planning/add-spicetify-skill/validation.md`
11. `docs/planning/add-spicetify-skill/codex-tooling.md`

First action: do read-only preflight. Confirm repository layout, package manager, current OpenSpec files, test commands, and write scopes. Update `docs/planning/add-spicetify-skill/context-map.md` and `PLANS.md` only if this task has write permission.

Use subagents only if this environment supports them and I have explicitly asked for swarm execution. If using subagents, spawn them according to `subagent-task-graph.md`:
- A0 repository-preflight first.
- After A0, run A1 contracts-and-schemas, A2 command-policy-state, A3 audit-provenance-security, A4 platform-repair-fixtures, and optionally A6 companion-docs-site in parallel only when their write scopes do not overlap.
- Run A5 modes-and-runtime-flows only after core contracts stabilize.
- Run A7 tests-validation-evals after enough implementation exists.
- Run A8 final-review-red-team last.

Each subagent must use the standard result envelope from `subagent-task-graph.md`. Wait for all requested subagents, consolidate their results, check for write-scope conflicts, and update `PLANS.md` with progress, discoveries, decisions, validation, blockers, and next steps.

If subagents are unavailable, use the single-agent fallback sequence in `subagent-task-graph.md` and produce one result envelope per phase.

Allowed write scope for planning-only kickoff:
- `docs/planning/add-spicetify-skill/context-map.md`
- `docs/planning/add-spicetify-skill/PLANS.md`
- `docs/planning/add-spicetify-skill/validation.md`
- review/report files requested by the user

Allowed write scope for implementation kickoff only after explicit approval:
- paths named in the assigned task from `openspec/changes/add-spicetify-skill/tasks.md`
- tests/fixtures/evals/schemas/doc paths that correspond to that task

Do not:
- install packages or run package-manager mutation without approval;
- access network without approval;
- run real `spicetify` or touch real Spotify/Spicetify paths in CI;
- run arbitrary shell or README-provided commands;
- commit, push, create PRs, deploy, modify permissions, enable MCP/hooks, or change cloud/account settings;
- read or request secrets;
- broaden the OpenSpec scope without stopping and reporting.

Validation to run or explain why not run:
```bash
python tools/validate_bundle.py --root .
python -m json.tool evals/regression-prompts.json >/dev/null
python - <<'PYCODE'
from pathlib import Path
import json
for p in Path('schemas').glob('*.json'):
    json.load(open(p))
print('schemas ok')
PYCODE
openspec validate add-spicetify-skill --strict
openspec validate --all --strict
```

Stop and report if required files are missing, specs contradict tasks, write scopes overlap, validation fails unexpectedly, secrets are needed, sandbox/approval policy is too broad or too narrow to proceed safely, a subagent asks to bypass policy, or implementation would touch real Spotify/Spicetify state.

Final response must include:
- tasks completed or reviewed;
- subagents used and their result-envelope summaries;
- changed files;
- validation results with exact command status;
- unresolved risks/blockers;
- next recommended task.

Do not claim success without validation evidence or an explicit note that a command could not be run.
```

## Kickoff variants

### Planning-only swarm

Use when the repo is not trusted for writes or the user wants a review only:

```text
Use the copyable prompt above, but keep all agents read-only except updates to `PLANS.md`, `context-map.md`, and a review report. Do not modify source code.
```

### Implementation swarm

Use when the user has approved implementation writes:

```text
Use the copyable prompt above. Assign write scopes by task ID from `tasks.md`. Spawn only agents whose write scopes do not overlap. Do not run package install or network commands without separate approval.
```

### Final review swarm

Use after implementation:

```text
Spawn review-only subagents for OpenSpec alignment, security/privacy, tests/fixtures, docs-site content, and UX. No code writes. Consolidate findings into severity-ranked fixes.
```

## Operator notes

- This prompt intentionally references paths instead of pasting the full bundle.
- Keep `AGENTS.md` durable and concise; task-specific details stay in OpenSpec, `PLANS.md`, and this kickoff file.
- If Codex reports a missing command surface or unsupported subagent feature, fall back to sequential execution and record it in `PLANS.md`.
