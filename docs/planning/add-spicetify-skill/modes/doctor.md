# Mode: doctor

**Path:** `docs/planning/add-spicetify-skill/modes/doctor.md`
**Purpose:** Detailed contract for `/spicetify doctor` mode.
**Status:** Proposed
**Load/use when:** Implementing, testing, or reviewing `doctor` behavior.

## Purpose

Diagnose broken, risky, or platform-incompatible Spicetify state.

## Inputs

`symptoms`, `scope`, `includeDevToolsLogs?`, `includeScreenshots?`, `redactionLevel`.

## Preconditions

Inspect can locate enough state to run checks; optional logs/screenshots require consent.

## Commands/files touched

Read-only probes plus optional redacted logs/screenshots. No config or asset writes.

## Safety checks

No mutation; logs/screenshots are consent-gated and redacted.

## Plan output

`DoctorPlan` with ranked checks, expected evidence, platform/package stop rules, and repair candidates.

## Execution flow

Run inspect; check config, paths, permissions symptoms, missing assets, invalid manifests, syntax errors, Marketplace presence, update symptoms.

## Verification flow

Each finding includes severity, evidence, confidence, and next safe mode.

## Rollback flow

None; no mutation.

## Idempotency notes

The planner MUST diff current state before emitting mutations. Re-running an already satisfied desired state SHOULD become a no-op plus verification unless the user explicitly requests refresh/reapply.

## Failure modes and recovery

- Unsupported platform/package -> report manual path; do not mutate.
- Log collection unavailable -> continue without logs and mark evidence skipped.


## Data contracts

Primary contracts: `request, operation-report, verification-report`. Any implementation-specific schema expansion MUST update `docs/planning/add-spicetify-skill/schemas/README.md`, `api-contracts.md`, and regression prompts.

## Cross-cutting controls

- Policy decision is required before execution, even for no-op verification plans.
- Secrets, prefs content, logs, screenshots, and private paths follow `privacy-redaction.md`.
- Third-party, Marketplace, imported, or unknown assets require provenance and audit before enablement.
- Desired-state or automation inputs cannot waive non-negotiable safety invariants.

## Example user prompts

- `/spicetify doctor after Spotify updated`
- `/spicetify why did Marketplace disappear?`

## Example structured response

```json
{
  "mode": "doctor",
  "risk": "read",
  "status": "degraded",
  "findings": [
    {
      "code": "SPOTIFY_UPDATED_REAPPLY_REQUIRED",
      "severity": "high"
    }
  ],
  "nextSafeMode": "repair"
}
```
