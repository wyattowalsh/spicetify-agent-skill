# Proposal: Build the `/spicetify` Skill

**Path:** `openspec/changes/add-spicetify-skill/proposal.md`
**Purpose:** Intent, scope, approach, impact, risks, and success criteria for the `/spicetify` skill.
**Status:** Proposed
**Load/use when:** Read before reviewing specs or tasks.

## Intent

Create `/spicetify`, a production-quality AI skill for local Spicetify power-user workflows. The skill SHALL expose semantic modes rather than raw shell access. It SHALL safely inspect, plan, snapshot, apply, verify, repair, and roll back customization state for themes, extensions, custom apps, snippets, Marketplace assets, profiles, config, and post-update recovery.

## Scope

### In scope

- A single user-facing skill named `/spicetify`.
- OpenSpec-backed behavior requirements and task graph.
- Typed command abstraction for allowlisted Spicetify CLI calls.
- Dry-run planner, policy engine, state/snapshot/rollback model.
- Config/profile management.
- Theme, extension, custom-app, snippet, and Marketplace workflows.
- Third-party code audit and provenance lock model.
- Doctor/repair workflows for Spotify update breakage and platform package issues.
- Verification using CLI output, filesystem checks, parsed config, optional screenshots, and optional redacted DevTools logs.
- JSON schemas for requests, plans, policy decisions, runs, reports, audits, snapshots, errors, provenance, fixtures, profiles, desired-state manifests, asset manifests, consent grants, and redaction policies.
- Fake Spicetify test strategy and no-live-Spotify CI guard.
- Companion Fumadocs documentation site plan with shadcn/ui customization, content architecture, safety-first examples, and docs validation gates.

### Out of scope

- Real Spotify mutation from generated tests.
- Spicetify/Spotify installation automation.
- Spotify account/DRM/ad/bypass behavior.
- Running arbitrary shell commands.
- Auto-running third-party install scripts, package-manager commands, permission changes, shortcut edits, or network downloads without explicit approval.
- Publishing to Marketplace or modifying remote GitHub repos.

## Approach

Use progressive disclosure:

1. Root docs orient humans and agents.
2. OpenSpec delta specs define behavior.
3. Design and workflow docs define implementation strategy.
4. Mode docs provide detailed per-mode contracts.
5. Schemas make plans and reports machine-checkable.
6. Codex handoff/Goal/PLANS make execution resumable and bounded.

The implementation ships as a Python package named `spicetify-agent`, preserves detected package managers, and uses fake Spicetify environments for CI. The companion docs app remains isolated under `docs`.

## Capabilities

- `skill` — route `/spicetify` prompts to semantic modes with progressive disclosure.
- `command` — compile safe operations into allowlisted Spicetify command invocations.
- `policy` — classify risks, confirmations, stops, idempotency, and approval gates.
- `state` — snapshot, restore, rollback, and maintain last-known-good state.
- `platform` — detect OS/package differences and unsafe repair preconditions.
- `config-profile` — model config and declarative profiles.
- `customization` — create/install/switch themes, extensions, custom apps, snippets, and Marketplace assets safely.
- `audit` — audit third-party code and prompt-injection risks before installation or enablement.
- `provenance` — lock source refs, hashes, audit verdicts, and accepted risks.
- `repair` — diagnose and repair known broken states, especially after Spotify updates.
- `devtools` — handle debugging, logs, screenshots, and launch flags with consent and redaction.
- `privacy` — minimize sensitive data capture and redact shareable evidence.
- `manifest` — export/import desired-state manifests with drift-aware replay.
- `scaffold` — generate maintained local templates and audit build outputs.
- `automation` — support headless dry-runs and batch plans without expanding authority.
- `verification` — verify and report every operation.
- `testing` — enforce fake environments and no live Spotify mutation in CI.
- `ux` — provide novice-safe and power-user structured experiences.
- `docs-site` — define the companion Fumadocs + shadcn/ui documentation site, content map, design system, validation gates, and source traceability.

## Impact

- Creates a durable OpenSpec source of truth for a local agent skill.
- Gives Codex a bounded implementation plan with clear stop conditions.
- Reduces risk of broken Spotify/Spicetify state after updates or third-party installs.
- Enables power-user automation through typed profiles, desired-state manifests, policy presets, redaction-aware reports, and provenance locks.
- Adds a documentation surface that makes safety, recovery, schemas, and mode behavior reviewable before implementation or real local use.

## Risks

| Risk | Severity | Mitigation |
|---|---|---|
| Real Spotify mutation during tests | High | Use fake Spicetify binary and fixture roots; require manual approval for real runs. |
| Third-party extension supply-chain risk | High | Stage, statically audit, lock provenance, score, and require confirmation before enabling. |
| Spicetify/Spotify update drift | High | Doctor/repair mode, source refresh before implementation, unsupported-build stop. |
| Platform-specific permission/package pitfalls | High | Platform matrix, read-only diagnostics, manual-only package/permission plans. |
| Overly large skill context | Medium | Keep `SKILL.md` compact; place depth in references, modes, workflows, schemas. |
| Config corruption | High | Prefer CLI config, transactional writes, snapshots, and rollback. |
| Ambiguous command behavior | Medium | Use allowlist registry, real/fake output parsers, and no raw shell passthrough. |
| DevTools/log leakage | High | Explicit consent, bounded collection, redaction, rollback launch flags. |
| Manifest replay surprise | High | Dry-run diff, non-waivable safety invariants, provenance locks, and exact plan-hash execution. |
| Scaffold supply-chain risk | High | Generated templates only by default, package-script approval, and built-output audit. |

## Open questions

- QUESTION-001: Which real repo will receive the generated implementation?
- QUESTION-002: Should the implementation ship as a Codex Skill only, a local CLI plus Skill, or both?
- QUESTION-003: Should optional screenshot verification be implemented in MVP or deferred?
- QUESTION-004: Should network GitHub install flows be deferred until local-mode MVP, provenance, and archive tests prove out?

## Success criteria

- `/spicetify` skill docs are concise and trigger-rich.
- OpenSpec requirements cover all required modes and safety principles.
- Tasks are dependency-aware with non-overlapping parallel slices.
- Schemas validate request/plan/report/audit/snapshot/profile/error/policy/provenance/manifest/privacy/consent shapes.
- MVP is implementable without live Spotify in CI.
- Every mutation path includes dry-run, snapshot, verification, and rollback.
- Companion docs-site requirements cover Fumadocs setup, shadcn/ui customization, content map, mode pages, schema pages, and docs validation.
- High-risk operations cannot execute without explicit, plan-hash-bound confirmation.

- `agents` — bounded subagent/swarm task graph, Codex kickoff prompt, result envelopes, and merge protocol.
