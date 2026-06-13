# Codex Goal: MVP `/spicetify`

**Path:** `docs/planning/add-spicetify-skill/goal.md`
**Purpose:** Bounded Codex Goal prompt for implementing the MVP safely.
**Status:** Proposed
**Load/use when:** Work is larger than one prompt but has a measurable finish line.

## Goal

Implement the MVP of `/spicetify` from OpenSpec change `add-spicetify-skill`.

## Done when

- `inspect`, `doctor`, `snapshot`, `audit`, `config`, `theme`, `profile`, `apply`, `repair`, `rollback`, and `report` are implemented or stubbed behind documented feature flags with passing tests.
- All mutating plans are dry-run-first and require policy decisions.
- All mutating executions require snapshots and support rollback.
- `CommandRegistry` is the only path to Spicetify CLI execution.
- Third-party code is staged, audited, and provenance-locked before installation or enablement.
- No tests mutate real Spotify/Spicetify.

## Read first
0. `docs/planning/add-spicetify-skill/codex-kickoff-prompt.md` for Codex swarm kickoff.
0. `docs/planning/add-spicetify-skill/subagent-task-graph.md` for bounded subagent assignments.

1. `AGENTS.md`
2. `openspec/changes/add-spicetify-skill/proposal.md`
3. `openspec/changes/add-spicetify-skill/tasks.md`
4. `openspec/changes/add-spicetify-skill/specs/`
5. `docs/planning/add-spicetify-skill/PLANS.md`
6. `docs/planning/add-spicetify-skill/mvp-cutline.md`
7. `docs/planning/add-spicetify-skill/policy-matrix.md`, `docs/planning/add-spicetify-skill/privacy-redaction.md`, `docs/planning/add-spicetify-skill/desired-state-manifest.md`
8. `docs/planning/add-spicetify-skill/codex-handoff.md`

## Constraints

- Use fake Spicetify fixtures for integration tests.
- No arbitrary shell; `spawn("spicetify", args, { shell:false })` only.
- No package-manager, network, permission, launch-flag, or publishing actions without approval.
- No secrets, real prefs content, or unredacted logs.
- Preserve `/spicetify` as the skill name.

## Progress logging

Update `docs/planning/add-spicetify-skill/PLANS.md` after each meaningful step with progress, discoveries, decisions, validation, changed files, and unresolved risks.

## Stop conditions

Stop for missing/contradictory specs, live Spotify mutation pressure, shell passthrough requirements, third-party script execution, secrets, unknown package-manager changes, validation failure without clear cause, or scope expansion.

## Final response expected

Summarize completed tasks, changed files, validation results, unresolved risks, and recommended next task.

## Docs-site goal addendum

Optional bounded goal: implement the accompanying Fumadocs + shadcn/ui documentation site only after runtime safety contracts are stable and package-manager approval is granted. Done when the docs app builds locally, core pages render, generated references are source-linked, search and AI-readable routes are present or explicitly deferred, and docs validation passes or failures are explained.

## Docs-site scope note

The goal includes planning and, when explicitly approved in a target repo, implementing the companion Fumadocs + shadcn/ui site. Package installs, network-backed shadcn registry actions, deployment, analytics, hosted search, and publishing remain approval-gated.
