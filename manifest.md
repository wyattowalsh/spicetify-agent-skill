# Manifest: `/spicetify`

**Path:** `manifest.md`
**Purpose:** Root artifact index and progressive-disclosure read map.
**Status:** Implemented baseline
**Load/use when:** Locating the source of truth for review or implementation.

## Source of truth

| Layer | Primary paths | Responsibility |
|---|---|---|
| OpenSpec behavior | `openspec/changes/add-spicetify-skill/specs/**/spec.md` | Observable requirements and scenarios. |
| Root design | `DESIGN.md` | Concise architecture for `/spicetify` and the companion docs site. |
| Change intent/design/tasks | `proposal.md`, `design.md`, `tasks.md` | Scope, architecture, implementation graph. |
| Human planning | `docs/planning/add-spicetify-skill/*.md` | Research, audit, tradeoffs, validation, examples, handoff. |
| Skill package | `skills/spicetify/` | Compact skill router and references. |
| Contracts | `schemas/*.schema.json` | Request/plan/run/report/audit/snapshot/profile/policy/manifest/privacy/consent/recovery/invariant schemas. |
| Regression | `evals/regression-prompts.json` | Behavior prompts for future plan and implementation audits. |

## Strengthened artifacts

| Path | Why it exists |
|---|---|
| `docs/planning/add-spicetify-skill/audit-review.md` | End-to-end critique, severity findings, and remediation decisions. |
| `docs/planning/add-spicetify-skill/source-refresh.md` | Current source table and verified-vs-assumed facts. |
| `docs/planning/add-spicetify-skill/platform-matrix.md` | OS/package-specific support and stop rules. |
| `docs/planning/add-spicetify-skill/threat-model.md` | Agent/security threat model and controls. |
| `docs/planning/add-spicetify-skill/policy-matrix.md` | Risk classification and confirmation gates. |
| `docs/planning/add-spicetify-skill/confirmation-flow.md` | Plan-bound confirmation grants and invalidation rules. |
| `docs/planning/add-spicetify-skill/privacy-redaction.md` | Data collection, redaction, snapshot, log, and screenshot boundaries. |
| `docs/planning/add-spicetify-skill/operation-state-machine.md` | Plan/execute/verify/rollback state transitions. |
| `docs/planning/add-spicetify-skill/invariants.md` | Non-waivable execution, privacy, state, audit, and CI invariants. |
| `docs/planning/add-spicetify-skill/failure-recovery-catalog.md` | Known failure modes, stop rules, recovery plans, and rollback behavior. |
| `docs/planning/add-spicetify-skill/cli-ux-contract.md` | Human and JSON interaction contract for dry-runs, confirmations, and errors. |
| `docs/planning/add-spicetify-skill/provenance-lockfile.md` | Third-party source lock and audit acceptance model. |
| `docs/planning/add-spicetify-skill/traceability.md` | Goals → requirements → tasks → validation map. |
| `docs/planning/add-spicetify-skill/acceptance-matrix.md` | User story → mode → spec → schema → test completion matrix. |
| `docs/planning/add-spicetify-skill/mvp-cutline.md` | Recommended implementation cutline and deferrals. |
| `docs/planning/add-spicetify-skill/desired-state-manifest.md` | Repeatable manifest import/export and replay model. |
| `docs/planning/add-spicetify-skill/scaffold-templates.md` | Maintained local templates and Creator compatibility boundary. |
| `docs/planning/add-spicetify-skill/automation-boundaries.md` | Headless and batch automation constraints. |
| `docs/planning/add-spicetify-skill/fumadocs-site-plan.md` | Full Fumadocs + shadcn/ui companion site plan. |
| `docs/planning/add-spicetify-skill/docs-site.md` | Docs-site overview and implementation guardrails. |
| `docs/planning/add-spicetify-skill/docs-content-architecture.md` | Content model, generated-reference pipeline, and editorial rules. |
| `docs/planning/add-spicetify-skill/docs-site-design-system.md` | shadcn/ui component and token plan for docs. |
| `docs/planning/add-spicetify-skill/docs-site-implementation-plan.md` | Dependency-aware docs-site implementation sequence. |

## Read order by use case

| Use case | Read |
|---|---|
| Fast review | `README.md`, `audit-review.md`, `proposal.md`, `tasks.md` |
| Security review | `threat-model.md`, `policy-matrix.md`, `specs/policy/spec.md`, `specs/audit/spec.md` |
| Spicetify fact review | `source-refresh.md`, `platform-matrix.md`, `research.md` |
| Implementation | `AGENTS.md`, `proposal.md`, `design.md`, `tasks.md`, `traceability.md`, `codex-handoff.md` |
| Docs site | `DESIGN.md`, `fumadocs-site-plan.md`, `docs-site.md`, `docs-content-architecture.md`, `docs-site-design-system.md`, `docs-site-implementation-plan.md`, `workflows/fumadocs-site.md`, `specs/docs-site`, `specs/docs-content`, `specs/docs-ui` |
| Skill packaging | `skills/spicetify/SKILL.md`, `skills/spicetify/references/*.md` |
| Test design | `validation.md`, `acceptance-matrix.md`, `specs/testing/spec.md`, `evals/regression-prompts.json` |

## Status

This repository contains the promoted planning artifacts, OpenSpec change,
schemas, skill docs, Python `spicetify-agent` implementation, fake-fixture
tests, validation tools, and isolated companion docs app. Real Spotify
mutation, network fetches, permission changes, Marketplace publishing,
dependency changes, pushes, PRs, and deployment remain approval-gated.

## Docs-site additions

| Path | Why it exists |
|---|---|
| `docs/planning/add-spicetify-skill/docs-site.md` | Companion Fumadocs + shadcn/ui site product plan. |
| `docs/planning/add-spicetify-skill/docs-site-content-map.md` | Full page tree and content acceptance rules. |
| `docs/planning/add-spicetify-skill/docs-site-design-system.md` | shadcn/ui tokens, components, variants, and copy rules. |
| `docs/planning/add-spicetify-skill/workflows/docs-site.md` | Earlier companion docs-site workflow; kept as compatible summary. |
| `DESIGN.md` | Root-level design narrative for the skill and accompanying docs site. |
| `docs/planning/add-spicetify-skill/fumadocs-site-plan.md` | Full Fumadocs + shadcn/ui site plan. |
| `docs/planning/add-spicetify-skill/docs-content-architecture.md` | Content model, navigation, generated references, and editorial workflow. |
| `docs/planning/add-spicetify-skill/docs-site-implementation-plan.md` | Implementation waves and validation for the docs app. |
| `docs/planning/add-spicetify-skill/workflows/fumadocs-site.md` | Cross-cutting docs-site workflow. |
| `openspec/changes/add-spicetify-skill/specs/docs-site/spec.md` | Behavior requirements for the docs app boundary. |
| `openspec/changes/add-spicetify-skill/specs/docs-content/spec.md` | Behavior requirements for docs content and generated references. |
| `openspec/changes/add-spicetify-skill/specs/docs-ui/spec.md` | Behavior requirements for Fumadocs UI and shadcn/ui integration. |

## Subagent/Codex swarm additions

| Path | Purpose | Status |
|---|---|---|
| `docs/planning/add-spicetify-skill/subagent-task-graph.md` | Bounded subagent DAG, roster, write scopes, result envelope, merge protocol, and fallback. | proposed |
| `docs/planning/add-spicetify-skill/codex-kickoff-prompt.md` | Copyable Codex kickoff prompt for swarm or sequential execution. | proposed |
| `docs/planning/add-spicetify-skill/workflows/subagent-swarm.md` | Operational workflow for subagent use and consolidation. | proposed |
| `openspec/changes/add-spicetify-skill/specs/agents/spec.md` | Behavior requirements for subagent task graph and kickoff prompt. | proposed |
| `schemas/subagent-task-graph.schema.json` | Machine-readable swarm task graph contract. | proposed |
| `schemas/subagent-result.schema.json` | Machine-readable subagent result envelope. | proposed |
