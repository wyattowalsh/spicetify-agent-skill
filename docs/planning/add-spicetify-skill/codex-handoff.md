# Codex handoff: implement `/spicetify`

**Path:** `docs/planning/add-spicetify-skill/codex-handoff.md`
**Purpose:** Compact execution prompt for Codex or a coding agent.
**Status:** Proposed
**Load/use when:** Ready to hand implementation/review work to a coding agent.

## Prompt

You are Codex implementing OpenSpec change `add-spicetify-skill`.

### Objective

Build `/spicetify`: a safe, transactional AI skill/local CLI architecture for Spicetify workflows. The MVP must inspect, doctor, snapshot, audit, plan, apply, verify, repair after Spotify updates, report, and rollback without arbitrary shell access or live Spotify mutation in CI.

### Done when

- Required MVP tasks through `TASK-042-implement-repair-spotify-update` are complete or explicitly deferred with evidence.
- All emitted JSON contracts validate against `schemas/*.schema.json`.
- Fake Spicetify integration tests cover healthy, broken, malicious, and post-update states.
- `spicetify` invocations are produced only by the registry with `shell: false`.
- Mutating operations are dry-run-first, snapshot-protected, policy-decided, verified, and rollbackable.
- Third-party code cannot install/enable without staging, audit, provenance, and explicit confirmation.

### Read first

1. `AGENTS.md`
2. `README.md`
3. `docs/planning/add-spicetify-skill/audit-review.md`
4. `openspec/changes/add-spicetify-skill/proposal.md`
5. `openspec/changes/add-spicetify-skill/tasks.md`
6. `openspec/changes/add-spicetify-skill/specs/`
7. `openspec/changes/add-spicetify-skill/design.md`
8. `docs/planning/add-spicetify-skill/context-map.md`
9. `docs/planning/add-spicetify-skill/policy-matrix.md`, `docs/planning/add-spicetify-skill/privacy-redaction.md`, `docs/planning/add-spicetify-skill/desired-state-manifest.md`
10. `docs/planning/add-spicetify-skill/invariants.md`
11. `docs/planning/add-spicetify-skill/failure-recovery-catalog.md`
12. `docs/planning/add-spicetify-skill/cli-ux-contract.md`
13. `docs/planning/add-spicetify-skill/operation-state-machine.md`
14. `docs/planning/add-spicetify-skill/provenance-lockfile.md`
15. `docs/planning/add-spicetify-skill/PLANS.md`

### Starting task

Start with `TASK-001-read-context`, then implement dependency waves in order. Do not jump to theme/extension features before command registry, policy, fake fixtures, and snapshots exist.

### Allowed write scope

For implementation in a future repo, write only to the approved project paths from `tasks.md`. For this planning bundle, write only to docs, schemas, evals, and validation tools unless the user explicitly requests production code.

### Prohibited actions

Do not install packages, run third-party scripts, access network, mutate real Spotify/Spicetify, edit permissions, edit launch flags, commit, push, publish, deploy, add hooks/MCP, or read secrets without explicit approval.

### Validation

Run or explain why unavailable:

```bash
python tools/validate_bundle.py --root .
python -m json.tool evals/regression-prompts.json >/dev/null
python - <<'PY'
from pathlib import Path
import json
for p in Path('schemas').glob('*.json'):
    json.load(open(p))
print('schemas ok')
PY
pnpm test
pnpm lint
pnpm typecheck
openspec validate add-spicetify-skill --strict
openspec validate --all --strict
```

### Stop conditions

Stop and report if:

- required planning files are missing or contradictory,
- OpenSpec specs conflict with task/design content,
- command implementation needs shell passthrough,
- a task requires live Spotify mutation in CI,
- third-party code must be executed to inspect/install,
- secrets or real prefs content are needed,
- package-manager, permission, network, launch-flag, hooks, MCP, publishing, or remote repo changes become necessary,
- validation fails unexpectedly,
- write scope would overlap another active agent.

### Final response

Report completed task IDs, changed files, validation results, unresolved risks, and next recommended task. Do not claim success without validation evidence.

## Docs-site handoff addendum

For TASK-070 through TASK-073, read `DESIGN.md`, `fumadocs-site-plan.md`, `docs-site.md`, `docs-content-architecture.md`, `docs-site-content-map.md`, `docs-site-design-system.md`, `docs-site-implementation-plan.md`, and `workflows/fumadocs-site.md` before editing. Write only under the approved docs app root and planning docs unless the handoff explicitly expands scope. Stop before package installation, package-manager migration, deployment, analytics, hosted search, external registries, feedback storage, or any generated content that would expose secrets/private paths. Do not install Fumadocs, shadcn/ui, or any package without explicit approval.

## Swarm kickoff

For broad implementation or review, start from `codex-kickoff-prompt.md` instead of pasting this whole bundle. Use `subagent-task-graph.md` to assign bounded subagents. Preserve non-overlapping write scopes, result envelopes, stop conditions, and orchestrator consolidation before any success claim.
