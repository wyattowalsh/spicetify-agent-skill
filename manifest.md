# Manifest: `/spicetify`

**Path:** `manifest.md`
**Purpose:** Root artifact index and progressive-disclosure read map.
**Status:** Implemented baseline
**Current release:** `v0.1.0`
**Load/use when:** Locating the source of truth for review or implementation.

## Source of truth

| Layer | Primary paths | Responsibility |
|---|---|---|
| OpenSpec behavior | `openspec/changes/add-spicetify-skill/specs/**/spec.md` | Observable requirements and scenarios. |
| Root design | `DESIGN.md` | Concise architecture for `/spicetify` and the companion docs site. |
| Change intent/design/tasks | `proposal.md`, `design.md`, `tasks.md` | Scope, architecture, implementation graph. |
| Human planning | `docs/content/docs/archive/add-spicetify-skill/*.mdx` | Research, audit, tradeoffs, validation, examples, handoff. |
| Skill package | `skills/spicetify/` | Compact skill router and references. |
| Skill distribution | `agent-bundle.json`, `.codex-plugin/plugin.json`, `.claude-plugin/plugin.json` | Single-skill source metadata for `npx skills add ... --skill spicetify` and metadata-only plugin discovery. |
| Release checklist | `CHANGELOG.md`, `RELEASE.md`, `docs/content/docs/reference/release-checklist.mdx` | Versioned release notes, validation commands, and public install verification. |
| Contracts | `skills/spicetify/assets/schemas/*.schema.json` | Request/plan/run/report/audit/snapshot/profile/policy/manifest/privacy/consent/recovery/invariant schemas. |
| Regression | `evals/regression-prompts.json` | Behavior prompts for future plan and implementation audits. |

## Strengthened artifacts

| Path | Why it exists |
|---|---|
| `docs/content/docs/archive/add-spicetify-skill/audit-review.mdx` | End-to-end critique, severity findings, and remediation decisions. |
| `docs/content/docs/archive/add-spicetify-skill/source-refresh.mdx` | Current source table and verified-vs-assumed facts. |
| `docs/content/docs/archive/add-spicetify-skill/platform-matrix.mdx` | OS/package-specific support and stop rules. |
| `docs/content/docs/archive/add-spicetify-skill/threat-model.mdx` | Agent/security threat model and controls. |
| `docs/content/docs/archive/add-spicetify-skill/policy-matrix.mdx` | Risk classification and confirmation gates. |
| `docs/content/docs/archive/add-spicetify-skill/confirmation-flow.mdx` | Plan-bound confirmation grants and invalidation rules. |
| `docs/content/docs/archive/add-spicetify-skill/privacy-redaction.mdx` | Data collection, redaction, snapshot, log, and screenshot boundaries. |
| `docs/content/docs/archive/add-spicetify-skill/operation-state-machine.mdx` | Plan/execute/verify/rollback state transitions. |
| `docs/content/docs/archive/add-spicetify-skill/invariants.mdx` | Non-waivable execution, privacy, state, audit, and CI invariants. |
| `docs/content/docs/archive/add-spicetify-skill/failure-recovery-catalog.mdx` | Known failure modes, stop rules, recovery plans, and rollback behavior. |
| `docs/content/docs/archive/add-spicetify-skill/cli-ux-contract.mdx` | Human and JSON interaction contract for dry-runs, confirmations, and errors. |
| `docs/content/docs/archive/add-spicetify-skill/provenance-lockfile.mdx` | Third-party source lock and audit acceptance model. |
| `docs/content/docs/archive/add-spicetify-skill/traceability.mdx` | Goals → requirements → tasks → validation map. |
| `docs/content/docs/archive/add-spicetify-skill/acceptance-matrix.mdx` | User story → mode → spec → schema → test completion matrix. |
| `docs/content/docs/archive/add-spicetify-skill/mvp-cutline.mdx` | Recommended implementation cutline and deferrals. |
| `docs/content/docs/archive/add-spicetify-skill/desired-state-manifest.mdx` | Repeatable manifest import/export and replay model. |
| `docs/content/docs/archive/add-spicetify-skill/scaffold-templates.mdx` | Maintained local templates and Creator compatibility boundary. |
| `docs/content/docs/archive/add-spicetify-skill/automation-boundaries.mdx` | Headless and batch automation constraints. |
| `docs/content/docs/archive/add-spicetify-skill/fumadocs-site-plan.mdx` | Full Fumadocs + shadcn/ui companion site plan. |
| `docs/content/docs/archive/add-spicetify-skill/docs-site.mdx` | Docs-site overview and implementation guardrails. |
| `docs/content/docs/archive/add-spicetify-skill/docs-content-architecture.mdx` | Content model, generated-reference pipeline, and editorial rules. |
| `docs/content/docs/archive/add-spicetify-skill/docs-site-design-system.mdx` | shadcn/ui component and token plan for docs. |
| `docs/content/docs/archive/add-spicetify-skill/docs-site-implementation-plan.mdx` | Dependency-aware docs-site implementation sequence. |

## Read order by use case

| Use case | Read |
|---|---|
| Fast review | `README.md`, `audit-review.md`, `proposal.md`, `tasks.md` |
| Security review | `threat-model.md`, `policy-matrix.md`, `specs/policy/spec.md`, `specs/audit/spec.md` |
| Spicetify fact review | `source-refresh.md`, `platform-matrix.md`, `research.md` |
| Implementation | `AGENTS.md`, `proposal.md`, `design.md`, `tasks.md`, `traceability.md`, `codex-handoff.md` |
| Docs site | `DESIGN.md`, `fumadocs-site-plan.md`, `docs-site.md`, `docs-content-architecture.md`, `docs-site-design-system.md`, `docs-site-implementation-plan.md`, `workflows/fumadocs-site.md`, `specs/docs-site`, `specs/docs-content`, `specs/docs-ui` |
| Skill packaging | `skills/spicetify/SKILL.md`, `skills/spicetify/references/*.md`, `agent-bundle.json`, `.codex-plugin/plugin.json`, `.claude-plugin/plugin.json` |
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
| `docs/content/docs/archive/add-spicetify-skill/docs-site.mdx` | Companion Fumadocs + shadcn/ui site product plan. |
| `docs/content/docs/archive/add-spicetify-skill/docs-site-content-map.mdx` | Full page tree and content acceptance rules. |
| `docs/content/docs/archive/add-spicetify-skill/docs-site-design-system.mdx` | shadcn/ui tokens, components, variants, and copy rules. |
| `docs/content/docs/archive/add-spicetify-skill/workflows/docs-site.mdx` | Earlier companion docs-site workflow; kept as compatible summary. |
| `DESIGN.md` | Root-level design narrative for the skill and accompanying docs site. |
| `docs/content/docs/archive/add-spicetify-skill/fumadocs-site-plan.mdx` | Full Fumadocs + shadcn/ui site plan. |
| `docs/content/docs/archive/add-spicetify-skill/docs-content-architecture.mdx` | Content model, navigation, generated references, and editorial workflow. |
| `docs/content/docs/archive/add-spicetify-skill/docs-site-implementation-plan.mdx` | Implementation waves and validation for the docs app. |
| `docs/content/docs/archive/add-spicetify-skill/workflows/fumadocs-site.mdx` | Cross-cutting docs-site workflow. |
| `openspec/changes/add-spicetify-skill/specs/docs-site/spec.md` | Behavior requirements for the docs app boundary. |
| `openspec/changes/add-spicetify-skill/specs/docs-content/spec.md` | Behavior requirements for docs content and generated references. |
| `openspec/changes/add-spicetify-skill/specs/docs-ui/spec.md` | Behavior requirements for Fumadocs UI and shadcn/ui integration. |

## Subagent/Codex swarm additions

| Path | Purpose | Status |
|---|---|---|
| `docs/content/docs/archive/add-spicetify-skill/subagent-task-graph.mdx` | Bounded subagent DAG, roster, write scopes, result envelope, merge protocol, and fallback. | proposed |
| `docs/content/docs/archive/add-spicetify-skill/codex-kickoff-prompt.mdx` | Copyable Codex kickoff prompt for swarm or sequential execution. | proposed |
| `docs/content/docs/archive/add-spicetify-skill/workflows/subagent-swarm.mdx` | Operational workflow for subagent use and consolidation. | proposed |
| `openspec/changes/add-spicetify-skill/specs/agents/spec.md` | Behavior requirements for subagent task graph and kickoff prompt. | proposed |
| `skills/spicetify/assets/schemas/subagent-task-graph.schema.json` | Machine-readable swarm task graph contract. | proposed |
| `skills/spicetify/assets/schemas/subagent-result.schema.json` | Machine-readable subagent result envelope. | proposed |
