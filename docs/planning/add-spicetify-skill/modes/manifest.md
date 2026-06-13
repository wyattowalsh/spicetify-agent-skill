# Mode: manifest

**Path:** `docs/planning/add-spicetify-skill/modes/manifest.md`
**Purpose:** Detailed contract for `/spicetify manifest` mode.
**Status:** Proposed
**Load/use when:** Implementing, testing, or reviewing desired-state manifest behavior.

## Purpose

Validate, explain, diff, or export declarative desired-state manifests without treating them as executable scripts.

## Inputs

Manifest path or inline manifest data, optional profile name, `diffCurrent?`, `exportCurrent?`.

## Preconditions

Manifest JSON parses; referenced local files are inside approved staging roots; third-party assets have provenance records before enablement.

## Commands/files touched

Reads manifest/profile/config metadata. Writes generated manifest files only when a separate mutating plan is approved.

## Safety checks

Dry-run first; schemas validate; unknown fields fail closed; desired-state data cannot waive policy, audit, provenance, snapshot, or confirmation gates.

## Plan output

`ManifestPlan` with schema verdict, normalized desired state, current-state diff, missing provenance, and follow-up mode suggestions.

## Execution flow

Parse manifest; validate schema; resolve references; compare to current state; emit dry-run plan or export artifact.

## Verification flow

Schema parse succeeds; resolved references stay under safe roots; generated report is redacted and source-traced.

## Rollback flow

None for read-only validation. Delete generated export files or restore snapshot if a separate export/apply plan writes them.

## Idempotency notes

The planner MUST diff current state before emitting mutations. Re-running an already satisfied desired state SHOULD become a no-op plus verification unless the user explicitly requests refresh/reapply.

## Failure modes and recovery

- Manifest schema invalid -> report exact schema path and stop.
- Referenced asset missing -> suggest audit/provenance staging before enablement.
- Desired state requests blocked action -> refuse; do not convert it into shell or package-manager commands.

## Data contracts

Primary contracts: `desired-state-manifest, asset-manifest, profile, operation-plan`. Any implementation-specific schema expansion MUST update `docs/planning/add-spicetify-skill/schemas/README.md`, `api-contracts.md`, and regression prompts.

## Cross-cutting controls

- Policy decision is required before execution, even for no-op verification plans.
- Secrets, prefs content, logs, screenshots, and private paths follow `privacy-redaction.md`.
- Third-party, Marketplace, imported, or unknown assets require provenance and audit before enablement.
- Desired-state or automation inputs cannot waive non-negotiable safety invariants.

## Example user prompts

- `/spicetify manifest validate desired-state.json`
- `/spicetify export my current setup as a manifest`

## Example structured response

```json
{
  "mode": "manifest",
  "schemaValid": true,
  "mutations": 0,
  "missingProvenance": []
}
```
