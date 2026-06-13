# Mode: theme

**Path:** `docs/planning/add-spicetify-skill/modes/theme.md`
**Purpose:** Detailed contract for `/spicetify theme` mode.
**Status:** Proposed
**Load/use when:** Implementing, testing, or reviewing `theme` behavior.

## Purpose

Create, validate, install, switch, watch, audit, or uninstall themes.

## Inputs

theme name, color scheme, source path/repo, CSS intent, `themeJsPolicy`.

## Preconditions

Theme root known; safe theme name; collisions handled by backup/confirmation.

## Commands/files touched

`Themes/<name>/color.ini`, `user.css`, optional `theme.js/assets`; config theme/scheme; apply/update/watch.

## Safety checks

CSS parse; block remote imports/URLs by default; audit `theme.js`; snapshot before install/switch.

## Plan output

`ThemePlan` listing generated/copied files, config diff, audit, verification, rollback.

## Execution flow

Generate/stage → validate/audit → snapshot → copy/write → config → apply/update.

## Verification flow

Required files exist; scheme exists; config points to theme; optional screenshot/log checks.

## Rollback flow

Restore previous config and remove skill-owned generated theme when requested.

## Idempotency notes

The planner MUST diff current state before emitting mutations. Re-running an already satisfied desired state SHOULD become a no-op plus verification unless the user explicitly requests refresh/reapply.

## Failure modes and recovery

- Remote CSS or theme.js risk -> audit/confirmation required.
- Collision with existing theme -> backup or stop.


## Data contracts

Primary contracts: `asset-manifest, audit-report, operation-plan`. Any implementation-specific schema expansion MUST update `docs/planning/add-spicetify-skill/schemas/README.md`, `api-contracts.md`, and regression prompts.

## Cross-cutting controls

- Policy decision is required before execution, even for no-op verification plans.
- Secrets, prefs content, logs, screenshots, and private paths follow `privacy-redaction.md`.
- Third-party, Marketplace, imported, or unknown assets require provenance and audit before enablement.
- Desired-state or automation inputs cannot waive non-negotiable safety invariants.

## Example user prompts

- `/spicetify create a dark terminal-style theme`
- `/spicetify install this GitHub theme safely`

## Example structured response

```json
{
  "mode": "theme",
  "action": "create",
  "theme": "TerminalDark",
  "risk": "medium",
  "files": [
    "color.ini",
    "user.css"
  ]
}
```

## Confirmation reference

Use `../confirmation-flow.md` whenever this mode crosses snapshot, mutation, destructive, third-party-code, DevTools, network, package-manager, permission, or launch-flag approval gates.
