# Mode: extension

**Path:** `docs/planning/add-spicetify-skill/modes/extension.md`
**Purpose:** Detailed contract for `/spicetify extension` mode.
**Status:** Proposed
**Load/use when:** Implementing, testing, or reviewing `extension` behavior.

## Purpose

Scaffold, build, audit, install, enable, debug, disable, or remove extensions.

## Inputs

extension source/name, scaffold spec, enable flag, trust level.

## Preconditions

Extension file/scaffold target valid; third-party audited before enable.

## Commands/files touched

`Extensions/<file>.js`; `spicetify config extensions <file>.js|<file>.js-`; apply; optional focused apply.

## Safety checks

No third-party package scripts by default; JS audit; provenance lock; snapshot before enable.

## Plan output

`ExtensionPlan` with scaffold/build/install/enable/debug steps and audit gate.

## Execution flow

Scaffold or stage → build approved local code → audit → lock provenance → copy → enable → apply.

## Verification flow

Config contains extension, file exists/hash, syntax parses, optional DevTools console redacted.

## Rollback flow

Remove config entry with trailing `-`; restore/delete installed file from snapshot.

## Idempotency notes

The planner MUST diff current state before emitting mutations. Re-running an already satisfied desired state SHOULD become a no-op plus verification unless the user explicitly requests refresh/reapply.

## Failure modes and recovery

- Audit block -> do not enable.
- Syntax/build failure -> keep staged files; no config mutation.


## Data contracts

Primary contracts: `asset-manifest, audit-report, consent-grant`. Any implementation-specific schema expansion MUST update `docs/planning/add-spicetify-skill/schemas/README.md`, `api-contracts.md`, and regression prompts.

## Cross-cutting controls

- Policy decision is required before execution, even for no-op verification plans.
- Secrets, prefs content, logs, screenshots, and private paths follow `privacy-redaction.md`.
- Third-party, Marketplace, imported, or unknown assets require provenance and audit before enablement.
- Desired-state or automation inputs cannot waive non-negotiable safety invariants.

## Example user prompts

- `/spicetify audit this extension before enabling it`
- `/spicetify scaffold a TypeScript React extension`

## Example structured response

```json
{
  "mode": "extension",
  "audit": "warn",
  "requiresConfirmation": true,
  "installAllowedByDefault": false
}
```

## Confirmation reference

Use `../confirmation-flow.md` whenever this mode crosses snapshot, mutation, destructive, third-party-code, DevTools, network, package-manager, permission, or launch-flag approval gates.
