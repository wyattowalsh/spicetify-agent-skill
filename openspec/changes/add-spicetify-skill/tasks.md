# Tasks: Build the `/spicetify` Skill

**Path:** `openspec/changes/add-spicetify-skill/tasks.md`
**Purpose:** Dependency-aware task graph for implementing and validating `/spicetify`.
**Status:** Active; safe MVP kernel implemented, deep workflow tasks remain tracked
**Load/use when:** Use as the primary implementation checklist.

## Legend

- `[P]` means parallel-safe: dependencies satisfied, no overlapping write scope, independent validation.
- Do not execute against real Spotify in automated tests.
- Commands are proposed until reviewed in a trusted repo.
- Every task must preserve `/spicetify` as the user-facing skill name.

## Current implementation note

As of 2026-06-13, the repository contains a runnable Python package,
`spicetify-agent`, an isolated docs app, fake Spicetify fixtures, generated
docs references, and tests for the core safety kernel. The unchecked task boxes
below remain intentional unless the exact task-level "Done when" criteria are
satisfied. In particular, full profile switching, theme file generation,
rollback restoration, extension/custom-app scaffolding, and platform fixture
matrices are still represented as contracts/plans rather than complete deep
workflow implementations.

## 0. Preflight and source grounding

- [ ] TASK-001-read-context
  - Goal: Read durable context before editing.
  - Read: `AGENTS.md`, `README.md`, `manifest.md`, `apps/docs/content/docs/archive/add-spicetify-skill/audit-review.mdx`, `source-refresh.md`, `proposal.md`, `design.md`, `specs/`, `context-map.md`
  - Write scope: none
  - Validation: required files exist
  - Done when: scope, risks, skill name `/spicetify`, and first task are clear

- [ ] TASK-002-ground-target-repo
  - Goal: Inspect the target repo before implementation.
  - Depends on: TASK-001-read-context
  - Read: repo tree, package manager files, existing tests, existing OpenSpec config, existing agent instructions
  - Write scope: `apps/docs/content/docs/archive/add-spicetify-skill/context-map.mdx`
  - Validation: context map updated with evidence, assumptions, detected package manager, command profile, and write scopes
  - Done when: implementation paths and detected commands are evidence-backed

- [ ] TASK-003-refresh-current-sources
  - Goal: Recheck volatile Spicetify/OpenSpec facts before implementation.
  - Depends on: TASK-001-read-context
  - Read: official Spicetify docs, Spicetify CLI changelog/source metadata, Spicetify Creator README, Marketplace wiki, OpenSpec docs/repo
  - Write scope: `apps/docs/content/docs/archive/add-spicetify-skill/source-refresh.mdx`, `research.md`, `context-map.md`
  - Validation: source table updated with checked date and conflicts
  - Done when: no “latest/current” claim is stale or uncited in planning docs

## 1. Contracts, policy, and fixtures

- [ ] TASK-010-add-core-schemas [P]
  - Goal: Add request, plan, command, mutation, report, error, audit, snapshot, run, policy, provenance, fixture, profile, invariant, and failure-recovery schemas.
  - Depends on: TASK-002-ground-target-repo
  - Read: `schemas/*.schema.json`, `api-contracts.md`, OpenSpec specs
  - Write scope: `src/schemas/`, `schemas/`, `tests/schemas/`
  - Validation: schema parse tests; valid/invalid fixture tests
  - Done when: invalid plans, reports, locks, and policy decisions fail validation

- [ ] TASK-011-add-command-registry-contracts [P]
  - Goal: Define allowlisted Spicetify command registry and argument validators.
  - Depends on: TASK-002-ground-target-repo
  - Read: `workflows/command-abstraction.md`, `specs/command/spec.md`
  - Write scope: `src/spicetify/`, `tests/command-registry/`
  - Validation: unknown commands, shell strings, invalid args, and combined raw commands are rejected
  - Done when: all command invocations use argv arrays and `shell: false`

- [ ] TASK-012-add-fake-spicetify-fixtures [P]
  - Goal: Create fake Spicetify binary and fake userdata roots.
  - Depends on: TASK-002-ground-target-repo
  - Read: `validation.md`, `specs/testing/spec.md`, `platform-matrix.md`
  - Write scope: `tests/fixtures/`, `scripts/fake-spicetify.*`, `tests/helpers/`
  - Validation: fake binary records argv, simulates success/failure, and CI guard blocks real paths
  - Done when: CI can test without real Spotify or Spicetify

- [ ] TASK-013-implement-policy-engine [P]
  - Goal: Implement risk classification, confirmations, blocked-action decisions, and idempotency rules.
  - Depends on: TASK-010-add-core-schemas
  - Read: `policy-matrix.md`, `threat-model.md`, `specs/policy/spec.md`
  - Write scope: `src/core/policy*`, `tests/policy/`
  - Validation: blocked install scripts, high-risk restore, plan drift, and no-op profile tests
  - Done when: no mutating plan can execute without a policy decision

- [ ] TASK-014-add-platform-diagnostics [P]
  - Goal: Model platform/package detection and stop rules.
  - Depends on: TASK-012-add-fake-spicetify-fixtures
  - Read: `platform-matrix.md`, `specs/platform/spec.md`
  - Write scope: `src/platform/`, `src/modes/doctor*`, `tests/platform/`
  - Validation: Windows Store, Scoop, Snap, Flatpak, APT/AUR, Homebrew, and Nix fixtures produce expected doctor findings
  - Done when: permission/package fixes are manual-only reports

- [ ] TASK-015-add-provenance-lock [P]
  - Goal: Implement provenance lock model for third-party/generated assets.
  - Depends on: TASK-010-add-core-schemas
  - Read: `provenance-lockfile.md`, `specs/provenance/spec.md`
  - Write scope: `src/provenance/`, `tests/provenance/`
  - Validation: source hash drift invalidates audit acceptance
  - Done when: third-party install plans require lockable source and audit metadata

- [ ] TASK-016-add-privacy-and-consent-contracts [P]
  - Goal: Implement redaction policies, consent grants, shareability labels, and final secret scanning contracts.
  - Depends on: TASK-010-add-core-schemas
  - Read: `privacy-redaction.md`, `specs/privacy/spec.md`, `schemas/redaction-policy.schema.json`, `schemas/consent-grant.schema.json`
  - Write scope: `src/privacy/`, `src/reports/`, `tests/privacy/`
  - Validation: token/path/log redaction tests; screenshot/log consent required; shareable report blocks on redaction failure
  - Done when: no report or debug evidence can persist sensitive content without redaction policy and consent metadata

- [ ] TASK-017-add-desired-state-manifest [P]
  - Goal: Implement desired-state manifest parsing, export, dry-run import, drift detection, and safety override rejection.
  - Depends on: TASK-010-add-core-schemas, TASK-015-add-provenance-lock
  - Read: `desired-state-manifest.md`, `automation-boundaries.md`, `specs/manifest/spec.md`, `specs/automation/spec.md`, `schemas/desired-state-manifest.schema.json`
  - Write scope: `src/manifest/`, `src/automation/`, `tests/manifest/`
  - Validation: export-current dry-run replay is no-op; unsafe manifest override blocked; missing third-party asset requires audit/provenance
  - Done when: manifests produce structured diffs and cannot bypass non-waivable invariants

- [ ] TASK-018-add-scaffold-template-contracts [P]
  - Goal: Implement generated template contracts and built-output audit requirements for extension/custom-app/theme scaffolds.
  - Depends on: TASK-010-add-core-schemas, TASK-013-implement-policy-engine
  - Read: `scaffold-templates.md`, `specs/scaffold/spec.md`, `workflows/extension-custom-app.md`, `workflows/audit.md`
  - Write scope: `src/scaffold/contracts*`, `tests/scaffold/contracts*`
  - Validation: template metadata requires built-output audit before install; imported package scripts require explicit approval in generated plans
  - Done when: scaffold contracts can generate safe local project plans without relying on deprecated tooling by default

- [ ] TASK-019-add-invariant-and-recovery-contracts [P]
  - Goal: Implement non-waivable invariant checks, failure recovery catalog handling, and recovery report fixtures.
  - Depends on: TASK-010-add-core-schemas, TASK-013-implement-policy-engine, TASK-012-add-fake-spicetify-fixtures
  - Read: `invariants.md`, `failure-recovery-catalog.md`, `specs/recovery/spec.md`, `schemas/invariant.schema.json`, `schemas/failure-recovery.schema.json`
  - Write scope: `src/core/invariants*`, `src/recovery/`, `tests/recovery/`, `tests/policy/`
  - Validation: invariant waiver tests; failure catalog fixtures; rollback-failure and manual-only recovery tests
  - Done when: unknown or unsafe recovery paths stop with a structured report and no prohibited side effects

## 2. Read-only MVP

- [ ] TASK-020-implement-skill-router
  - Goal: Implement `/spicetify` routing and mode classification.
  - Depends on: TASK-010-add-core-schemas, TASK-013-implement-policy-engine
  - Read: `skills/spicetify/SKILL.md`, `mode-catalog.md`, `specs/skill/spec.md`
  - Write scope: `skills/spicetify/`, `src/intent/`, `tests/intent/`
  - Validation: prompt fixtures route to expected modes; unsupported raw-shell prompts are blocked or redirected
  - Done when: `/spicetify` is the only visible skill name

- [ ] TASK-021-implement-inspect-doctor-report
  - Goal: Implement read-only inspect, doctor, and report.
  - Depends on: TASK-011-add-command-registry-contracts, TASK-012-add-fake-spicetify-fixtures, TASK-014-add-platform-diagnostics
  - Read: mode docs for `inspect`, `doctor`, `report`; `platform-matrix.md`
  - Write scope: `src/modes/inspect*`, `src/modes/doctor*`, `src/reports/`, `tests/integration/inspect-doctor/`
  - Validation: fake healthy and broken env tests; no mutation occurs in read-only modes
  - Done when: diagnostics include evidence, severity, safe next action, and platform stop rules

- [ ] TASK-022-implement-audit-readonly
  - Goal: Implement static audit for JS/CSS/manifest/README sources.
  - Depends on: TASK-010-add-core-schemas, TASK-015-add-provenance-lock
  - Read: `workflows/audit.md`, `modes/audit.md`, `specs/audit/spec.md`
  - Write scope: `src/audit/`, `tests/audit/`
  - Validation: malicious extension fixture is blocked; CSS-only theme fixture passes; prompt-injection README is reported
  - Done when: audit reports include evidence, severity, recommendation, and provenance linkage


- [ ] TASK-024-implement-confirmation-contract
  - Goal: Implement plan-bound confirmation grants and invalidation semantics.
  - Depends on: TASK-010-add-core-schemas, TASK-013-implement-policy-engine
  - Read: `schemas/confirmation.schema.json`, `apps/docs/content/docs/archive/add-spicetify-skill/confirmation-flow.mdx`, `specs/policy/spec.md`, `specs/state/spec.md`
  - Write scope: confirmation/policy/run-record modules and tests
  - Validation: plan hash mismatch invalidates confirmation before mutation
  - Done when: confirmation grants are persisted, scoped, expiring, revocable, and reportable

- [ ] TASK-025-implement-redaction-boundaries
  - Goal: Implement privacy/redaction rules for reports, logs, screenshots, snapshots, and doctor evidence.
  - Depends on: TASK-010-add-core-schemas, TASK-013-implement-policy-engine
  - Read: `apps/docs/content/docs/archive/add-spicetify-skill/privacy-redaction.mdx`, `specs/policy/spec.md`, `specs/verification/spec.md`
  - Write scope: redaction/report/snapshot/log modules and tests
  - Validation: token-like strings, prefs content, cookies, auth headers, and private paths are masked in shareable reports
  - Done when: sensitive evidence cannot be persisted or reported without consent and redaction

## 3. State, config, and profiles

- [ ] TASK-030-implement-snapshot-store
  - Goal: Implement immutable snapshots, hash manifests, exclusions, and last-known-good pointer.
  - Depends on: TASK-021-implement-inspect-doctor-report
  - Read: `operation-state-machine.md`, `workflows/state-snapshots-rollback.md`, `specs/state/spec.md`
  - Write scope: `src/state/`, `tests/state/`
  - Validation: snapshot/restore hash tests; prefs/log exclusion tests
  - Done when: failed snapshot blocks mutation

- [ ] TASK-031-implement-config-model
  - Goal: Parse, diff, and edit config safely.
  - Depends on: TASK-030-implement-snapshot-store
  - Read: `workflows/config-profile.md`, `specs/config-profile/spec.md`
  - Write scope: `src/spicetify/config*`, `src/modes/config*`, `tests/config/`
  - Validation: config round-trip, protected patch tests, CLI-preferred config mutations
  - Done when: config edits prefer CLI commands and exact-list edits are transactional

- [ ] TASK-032-implement-profile-switching
  - Goal: Implement declarative exact-state profiles and profile export.
  - Depends on: TASK-031-implement-config-model, TASK-015-add-provenance-lock, TASK-017-add-desired-state-manifest
  - Read: `modes/profile.md`, `schemas/profile.schema.json`
  - Write scope: `src/modes/profile*`, `src/profile/`, `tests/profile/`
  - Validation: minimal/dev/visualizer fixture switches and rollbacks; repeated switch is no-op
  - Done when: profile diffs add/remove only planned values and audit third-party references

## 4. Mutating MVP

- [ ] TASK-040-implement-apply-and-rollback
  - Goal: Execute approved plans with snapshot, command/file transactions, verification, and rollback.
  - Depends on: TASK-013-implement-policy-engine, TASK-016-add-privacy-and-consent-contracts, TASK-030-implement-snapshot-store, TASK-031-implement-config-model
  - Read: `operation-state-machine.md`, `modes/apply.md`, `modes/rollback.md`
  - Write scope: `src/core/`, `src/modes/apply*`, `src/modes/rollback*`, `tests/integration/apply-rollback/`
  - Validation: failed apply auto-stops and rollback succeeds in fake env; plan hash drift blocks execution
  - Done when: every mutating run emits an operation report

- [ ] TASK-041-implement-theme-workflow
  - Goal: Create, validate, install-local, switch, update, and remove themes.
  - Depends on: TASK-040-implement-apply-and-rollback, TASK-022-implement-audit-readonly
  - Read: `workflows/theme.md`, `modes/theme.md`, `specs/customization/spec.md`
  - Write scope: `src/modes/theme*`, `src/theme/`, `tests/theme/`
  - Validation: dark terminal-style theme generated and verified in fake env; overwrite requires backup and confirmation
  - Done when: theme operations are idempotent and rollbackable

- [ ] TASK-042-implement-repair-spotify-update
  - Goal: Implement safe post-Spotify-update repair plan.
  - Depends on: TASK-040-implement-apply-and-rollback, TASK-014-add-platform-diagnostics
  - Read: `modes/repair.md`, `workflows/doctor-repair.md`, `specs/repair/spec.md`
  - Write scope: `src/modes/repair*`, `tests/repair/`
  - Validation: backup/apply path runs; restore fallback requires separate confirmation; unsupported build stops safely
  - Done when: repair is staged, snapshot-protected, and honest about unsupported Spotify updates

## 5. Developer and third-party workflows

- [ ] TASK-050-implement-extension-custom-app-scaffolds
  - Goal: Add generated TypeScript templates for extensions and custom apps.
  - Depends on: TASK-018-add-scaffold-template-contracts, TASK-022-implement-audit-readonly, TASK-040-implement-apply-and-rollback
  - Read: `workflows/extension-custom-app.md`, `modes/extension.md`, `modes/custom-app.md`
  - Write scope: `src/scaffold/`, `src/modes/extension*`, `src/modes/custom-app*`, `tests/scaffold/`
  - Validation: generated fixtures build with approved local commands only; third-party repos are not built or script-run by default
  - Done when: Creator compatibility is optional and warns about deprecation

- [ ] TASK-051-implement-snippet-marketplace-safe-flows
  - Goal: Add snippet and Marketplace inspect/audit/install-plan flows.
  - Depends on: TASK-041-implement-theme-workflow, TASK-015-add-provenance-lock
  - Read: `modes/snippet.md`, `modes/marketplace.md`, `specs/provenance/spec.md`
  - Write scope: `src/modes/snippet*`, `src/modes/marketplace*`, `tests/marketplace/`
  - Validation: install scripts are blocked; staged repo audit works; valid Marketplace manifest is not treated as trust
  - Done when: Marketplace flows are safe manual/file plans, not script passthrough

- [ ] TASK-052-implement-devtools-watch-update-migrate-uninstall
  - Goal: Implement advanced modes behind approval gates.
  - Depends on: TASK-050-implement-extension-custom-app-scaffolds, TASK-013-implement-policy-engine
  - Read: mode docs for `devtools`, `watch`, `update`, `migrate`, `uninstall`; `specs/devtools/spec.md`
  - Write scope: `src/modes/devtools*`, `watch*`, `update*`, `migrate*`, `uninstall*`, `tests/advanced/`
  - Validation: high-risk actions require confirmation; logs redact secrets; watchers are bounded
  - Done when: advanced modes are useful but cannot surprise-mutate

## 6. UX, docs, and reports

- [ ] TASK-060-add-ux-examples-and-human-docs [P]
  - Goal: Add examples for novice and power-user workflows.
  - Depends on: TASK-041-implement-theme-workflow
  - Read: `ux-examples.md`, `specs/ux/spec.md`
  - Write scope: `README.md`, `docs/`, `examples/`
  - Validation: examples map to passing regression prompts and include structured output
  - Done when: example outputs are consistent and confirmation copy names exact effects

- [ ] TASK-061-add-operation-reports [P]
  - Goal: Emit JSON and Markdown operation reports.
  - Depends on: TASK-040-implement-apply-and-rollback
  - Read: `schemas/operation-report.schema.json`, `schemas/verification-report.schema.json`, `privacy-redaction.md`
  - Write scope: `src/reports/`, `tests/reports/`
  - Validation: secret-redaction tests; report schema tests
  - Done when: reports include plan, run, verification, rollback, provenance, and next actions



## 7. Docs site companion

- [ ] TASK-070-plan-docs-site-contracts
  - Goal: Add Fumadocs + shadcn/ui site contracts, source grounding, and target repo decisions.
  - Depends on: TASK-003-refresh-current-sources, TASK-010-add-core-schemas
  - Read: `DESIGN.md`, `fumadocs-site-plan.md`, `docs-site.md`, `docs-content-architecture.md`, `docs-site-content-map.md`, `docs-site-design-system.md`, `docs-site-implementation-plan.md`, `workflows/fumadocs-site.md`, `specs/docs-site/spec.md`, `specs/docs-content/spec.md`, `specs/docs-ui/spec.md`
  - Write scope: docs-site planning docs, docs-site schemas, OpenSpec docs-site specs
  - Validation: bundle validator; JSON schema parse; OpenSpec validation
  - Done when: docs-site app root, content root, route map, component policy, generated-content policy, and stop conditions are explicit

- [ ] TASK-071-implement-docs-content-source
  - Goal: Implement Fumadocs content source and curated core pages after package-manager approval.
  - Depends on: TASK-070-plan-docs-site-contracts
  - Read: `docs-content-architecture.md`, target repo package files, Fumadocs setup docs
  - Write scope: approved docs app root such as `apps/docs/`, generated docs directory, docs package metadata
  - Validation: docs content validation; internal link checks; no-placeholder/no-secret checks
  - Done when: overview, quickstart, safety, mode catalog, and workflow pages render from local content

- [ ] TASK-072-implement-docs-ui-shadcn
  - Goal: Configure Fumadocs UI with shadcn-compatible theme tokens and local components.
  - Depends on: TASK-071-implement-docs-content-source
  - Read: `fumadocs-site-plan.md`, `specs/docs-ui/spec.md`, target repo style conventions
  - Write scope: docs app styles, `components/ui/`, `components/spicetify/`, `components/mdx.tsx`, `components.json`
  - Validation: docs typecheck/build; accessibility checks; local component provenance review
  - Done when: Fumadocs docs chrome and local shadcn components share theme tokens and keyboard-accessible interactions

- [ ] TASK-073-implement-docs-generated-references-search-llms
  - Goal: Add generated references, local search, and AI-readable docs routes.
  - Depends on: TASK-071-implement-docs-content-source, TASK-072-implement-docs-ui-shadcn
  - Read: `schemas/`, `modes/`, `specs/`, `traceability.md`, Fumadocs search and LLM docs
  - Write scope: docs generation scripts, generated docs directory, docs search route, docs LLM routes
  - Validation: deterministic generated diff; redaction checks; docs build; search route smoke test; LLM routes omit private evidence
  - Done when: generated reference pages link to source paths and AI-readable routes are safe or explicitly deferred

## 8. Subagent swarm and Codex kickoff

- [ ] TASK-080-add-subagent-task-graph [P]
  - Goal: Add and validate the bounded Codex subagent graph.
  - Depends on: TASK-002-ground-target-repo
  - Read: `apps/docs/content/docs/archive/add-spicetify-skill/codex-tooling.mdx`, `apps/docs/content/docs/archive/add-spicetify-skill/context-map.mdx`, `specs/agents/spec.md`
  - Write scope: `apps/docs/content/docs/archive/add-spicetify-skill/subagent-task-graph.mdx`, `schemas/subagent-task-graph.schema.json`, `schemas/subagent-result.schema.json`
  - Validation: graph contains orchestrator, A0 through A8, non-overlapping write scopes, result envelope, merge protocol, and sequential fallback
  - Done when: Codex can assign subagents without overlapping writes or missing stop conditions

- [ ] TASK-081-add-codex-kickoff-prompt [P]
  - Goal: Add a copyable Codex prompt for swarm, planning-only, implementation, and final-review kickoff.
  - Depends on: TASK-080-add-subagent-task-graph
  - Read: `AGENTS.md`, `README.md`, `DESIGN.md`, `tasks.md`, `subagent-task-graph.md`, `validation.md`
  - Write scope: `apps/docs/content/docs/archive/add-spicetify-skill/codex-kickoff-prompt.mdx`, `apps/docs/content/docs/archive/add-spicetify-skill/codex-handoff.mdx`, `apps/docs/content/docs/archive/add-spicetify-skill/goal.mdx`
  - Validation: prompt includes read-first files, write scopes, validation commands, stop conditions, and final response contract
  - Done when: the prompt can be pasted into Codex without requiring chat history

- [ ] TASK-082-add-subagent-validation-and-evals [P]
  - Goal: Extend validation and deterministic eval coverage for swarm behavior, `/spicetify` mode routing, fake fixtures, and `evolve`.
  - Depends on: TASK-080-add-subagent-task-graph, TASK-081-add-codex-kickoff-prompt
  - Read: `validation.md`, `eval-stack.md`, `evals/regression-prompts.json`, `evals/spicetify-eval-suite.json`, `schemas/eval-*.schema.json`, `tools/validate_bundle.py`
  - Write scope: `tools/validate_bundle.py`, `tools/run_skill_evals.py`, `evals/`, `tests/fixtures/evals/`, `tests/test_eval_contracts.py`, `tests/evals/`, eval schemas, and eval docs
  - Validation: bundle validator checks swarm files/schemas/spec; eval prompts parse; eval suite rejects missing fixtures, invalid traces, bogus artifacts, and unsafe activation; fake execution uses only approved fake fixtures
  - Done when: missing swarm/eval artifacts fail validation and valid fake-only artifacts pass strict local evals

## 9. Validation and implementation readiness

- [ ] TASK-090-run-validation
  - Goal: Validate OpenSpec, schemas, tests, examples, and readiness docs.
  - Depends on: TASK-052-implement-devtools-watch-update-migrate-uninstall, TASK-060-add-ux-examples-and-human-docs, TASK-061-add-operation-reports, TASK-073-implement-docs-generated-references-search-llms, TASK-082-add-subagent-validation-and-evals
  - Read: all changed files
  - Write scope: docs/status only if needed
  - Validation:
    ```bash
    openspec validate add-spicetify-skill --strict
    openspec validate --all --strict
    python tools/validate_bundle.py --root .
    pnpm test
    pnpm lint
    pnpm typecheck
    pnpm --filter docs build
    ```
  - Done when: validation passes or every failure is documented with owner and next step

- [ ] TASK-095-prepare-archive-readiness
  - Goal: Document whether implementation is ready for verify/sync/archive.
  - Depends on: TASK-090-run-validation
  - Write scope: `apps/docs/content/docs/archive/add-spicetify-skill/validation.mdx`, `apps/docs/content/docs/archive/add-spicetify-skill/acceptance-matrix.mdx`, `PLANS.md`
  - Validation: no archive action performed without user approval
  - Done when: archive criteria and blockers are explicit
