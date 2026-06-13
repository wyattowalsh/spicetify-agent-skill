---
name: spicetify
description: Use when the user asks for `/spicetify` help with safe local Spicetify workflows: inspect, doctor, snapshot, restore, repair, apply, config, profile, theme, extension, custom-app, snippet, marketplace, audit, devtools, watch, migrate, update, rollback, uninstall, or report. Always plan/dry-run before mutation and never expose arbitrary shell access.
---

# /spicetify

**Path:** `skills/spicetify/SKILL.md`
**Purpose:** Compact router for safe local Spicetify operations.
**Status:** Proposed
**Load/use when:** The user invokes or asks about `/spicetify`.

## Use when

The user wants to inspect, plan, modify, apply, debug, repair, audit, or roll back Spotify/Spicetify customizations through high-level semantic modes.

## Not for

- Spotify account, DRM, subscription, ad-blocking, or bypass behavior.
- Arbitrary shell execution or user-provided command passthrough.
- Running installer scripts from READMEs, Marketplace metadata, or third-party repos.
- Reading secrets, tokens, cookies, credentials, or Spotify prefs contents.
- Mutating real Spotify/Spicetify in CI or without explicit approval.
- Package-manager actions, permission changes, shortcut edits, launch-flag edits, publishing, or remote repo changes unless separately approved.

## Router workflow

1. Classify the request into one or more modes.
2. Use read-only probes first when local state matters.
3. For possible mutation, produce a dry-run `OperationPlan` with policy decision, plan hash, snapshot requirement, verification, and rollback path.
4. Stage and audit third-party code before install/enable.
5. Require snapshot and explicit confirmation before execution.
6. Execute only allowlisted Spicetify argv shapes with `shell:false`.
7. Verify with CLI output, parsed config, filesystem hashes, audit/provenance checks, optional screenshots, and optional redacted DevTools logs.
8. Update last-known-good only after required verification passes.
9. Report results, risks, and rollback path.

## Modes

`inspect`, `doctor`, `snapshot`, `restore`, `repair`, `apply`, `config`, `profile`, `theme`, `extension`, `custom-app`, `snippet`, `marketplace`, `audit`, `devtools`, `watch`, `migrate`, `update`, `rollback`, `uninstall`, `report`.

## Compact mode routing

- “What is installed / what is broken?” → `inspect` or `doctor`.
- “Spotify updated and Spicetify broke” → `repair` with doctor + snapshot + backup/apply plan.
- “Change config / switch setup” → `config` or `profile`.
- “Create/install/switch theme” → `theme` plus audit if third-party.
- “Enable extension/custom app” → `audit` first, then `extension` or `custom-app`.
- “Install from GitHub/Marketplace” → `audit` + `provenance` + dry-run install plan.
- “Debug logs/UI” → `devtools` with explicit consent and redaction.
- “Undo” → `rollback` or `restore`.

## References

- `references/mode-router.md`
- `references/safety-policy.md`
- `references/spicetify-facts.md`
- `references/examples.md`
- `../../apps/docs/content/docs/`
- `../../apps/docs/docs-site-manifest.json`
- `../../docs/planning/add-spicetify-skill/mode-catalog.md`
- `../../docs/planning/add-spicetify-skill/modes/`
- `../../docs/planning/add-spicetify-skill/workflows/`
- `../../schemas/`

## Default response stance

- Read-only requests: answer directly with evidence and safe next actions.
- Mutating requests: dry-run first; do not execute.
- Dangerous requests: refuse the unsafe part and offer safe diagnostics or a manual checklist.
