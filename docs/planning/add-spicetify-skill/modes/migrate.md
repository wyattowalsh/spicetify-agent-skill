# Mode: migrate

**Path:** `docs/planning/add-spicetify-skill/modes/migrate.md`
**Purpose:** Detailed contract for `/spicetify migrate` mode.
**Status:** Proposed
**Load/use when:** Implementing, testing, or reviewing `migrate` behavior.

## Purpose

Convert ad hoc state into manifests/profiles or migrate /spicetify schema compatibility states.

## Inputs

source config/snapshot/profile schema, target schema, writeManifests?`.

## Preconditions

Inspect/snapshot available; source parses.

## Commands/files touched

Reads config/assets; writes /spicetify manifests only if requested.

## Safety checks

Dry-run by default; no config mutation unless separately planned.

## Plan output

`MigrationPlan` with inferred profiles, unknowns, generated files, validation.

## Execution flow

Parse current state → infer profiles/locks → write manifests if approved → validate.

## Verification flow

Dry-run replay equals current state; schemas validate.

## Rollback flow

Delete generated manifests or restore snapshot if applied.

## Idempotency notes

The planner MUST diff current state before emitting mutations. Re-running an already satisfied desired state SHOULD become a no-op plus verification unless the user explicitly requests refresh/reapply.

## Failure modes and recovery

- Schema incompatibility -> emit dry-run migration report only.
- Declarative ownership -> prefer export, not mutation.


## Data contracts

Primary contracts: `desired-state-manifest, profile, provenance-lock`. Any implementation-specific schema expansion MUST update `docs/planning/add-spicetify-skill/schemas/README.md`, `api-contracts.md`, and regression prompts.

## Cross-cutting controls

- Policy decision is required before execution, even for no-op verification plans.
- Secrets, prefs content, logs, screenshots, and private paths follow `privacy-redaction.md`.
- Third-party, Marketplace, imported, or unknown assets require provenance and audit before enablement.
- Desired-state or automation inputs cannot waive non-negotiable safety invariants.

## Example user prompts

- `/spicetify migrate my current setup into profiles`

## Example structured response

```json
{
  "mode": "migrate",
  "generatedProfiles": [
    "current",
    "minimal"
  ],
  "mutations": 0
}
```
