# Implementation plan

**Path:** `docs/planning/add-spicetify-skill/implementation-plan.md`
**Purpose:** Milestones, sequencing, rollout, rollback, and acceptance checks.
**Status:** Draft
**Load/use when:** Use to coordinate implementation beyond the task checklist.


## Milestones

### M1 — Contracts and fake environment

**Goal:** Make safety testable before adding mutation.
**Outputs:** schemas, command registry, fake binary, fixtures.
**Exit criteria:** unknown commands and shell strings fail tests.

### M2 — Read-only core

**Goal:** Inspect, doctor, audit, and report without mutation.
**Outputs:** mode router, read-only probes, static audit.
**Exit criteria:** broken fixtures produce useful diagnostics and no writes.

### M3 — Snapshot/config/profile

**Goal:** Protect and model user state.
**Outputs:** snapshot store, config parser/diff, profiles.
**Exit criteria:** snapshot/restore hash tests and profile diff tests pass.

### M4 — Apply/rollback/theme/repair MVP

**Goal:** Deliver the useful MVP.
**Outputs:** dry-run/apply/rollback, theme creation, Spotify-update repair.
**Exit criteria:** fake env can create terminal theme, apply, verify, and roll back.

### M5 — Developer and third-party workflows

**Goal:** Support extension/custom app scaffolds, snippets, Marketplace-safe flows.
**Outputs:** templates, audit-gated install plans, devtools/watch/update/migrate/uninstall.
**Exit criteria:** risky third-party code is blocked; generated local code can be built with approved local commands.

### M6 — Docs/evals/implementation readiness

**Goal:** Make the skill maintainable.
**Outputs:** docs, examples, reports, regression prompts.
**Exit criteria:** OpenSpec, unit, integration, schema, and eval checks pass.

### M7 — Rigorous eval stack and evolve mode

**Goal:** Turn evals into an improvement loop for `/spicetify`.
**Outputs:** eval-case/suite/result/trace contracts, fake-only local runner, deterministic graders, mode-complete eval suites, and `/spicetify evolve` reports.
**Exit criteria:** every mode has structured happy-path, blocked-path, trigger, recovery/report, and hard-safety evals; `evolve` produces ranked eval-first improvement plans without self-applying or weakening safety.

## Sequencing rationale

Start with contracts and fake environments because real Spotify mutation is high risk. Add mutating modes only after snapshots, config parsing, command allowlists, and verification infrastructure exist.

## Rollback / repair

Implementation rollback is normal Git/document rollback. Runtime rollback is snapshot-based and tested in fake env. Failed implementation discoveries update `PLANS.md`, then `design.md`/`tasks.md` as needed.

## Documentation-site milestone

### M-DOCS — Companion Fumadocs site with shadcn/ui
**Goal:** Add and, when approved in a target repo, implement a Fumadocs site that documents `/spicetify` modes, safety, schemas, workflows, recovery, and examples.
**Inputs:** `DESIGN.md`, `fumadocs-site-plan.md`, `docs-content-architecture.md`, `docs-site-design-system.md`, `docs-site-implementation-plan.md`, `workflows/fumadocs-site.md`.
**Outputs:** Fumadocs app files, shadcn/ui component baseline, custom docs components, MDX content tree, schema reference pages, docs validation report.
**Tasks:** TASK-070 through TASK-073.
**Exit criteria:** Docs build/type/lint/link/accessibility/redaction checks pass or failures are documented with owners.

### M-SWARM — Subagent-optimized Codex execution
**Goal:** Enable safe Codex swarm execution without weakening OpenSpec, policy, or write-scope controls.
**Inputs:** `subagent-task-graph.md`, `codex-kickoff-prompt.md`, `workflows/subagent-swarm.md`, `specs/agents/spec.md`.
**Outputs:** bounded agent assignments, result envelopes, merge protocol, sequential fallback, and validation gates.
**Tasks:** TASK-080 through TASK-082.
**Exit criteria:** Codex can start from the kickoff prompt, spawn or emulate bounded subagents, consolidate results, run validation, and stop on overlap or approval needs.
