# Mode: report

**Path:** `docs/planning/add-spicetify-skill/modes/report.md`
**Purpose:** Detailed contract for `/spicetify report` mode.
**Status:** Proposed
**Load/use when:** Implementing, testing, or reviewing `report` behavior.

## Purpose

Produce shareable redacted operation, audit, doctor, or profile reports.

## Inputs

`reportType`, `includeEvidence?`, `redactionLevel`, source run/audit/snapshot IDs.

## Preconditions

Relevant data exists; optional logs/screenshots consented.

## Commands/files touched

Writes report JSON/Markdown only.

## Safety checks

Secret scanner before writing/sharing; no unredacted prefs/logs by default.

## Plan output

`ReportPlan` listing included evidence, redaction level, output paths.

## Execution flow

Gather records → redact → render → validate schema → scan for secrets.

## Verification flow

Schema valid; redaction performed; paths exist.

## Rollback flow

Delete generated report if requested.

## Idempotency notes

The planner MUST diff current state before emitting mutations. Re-running an already satisfied desired state SHOULD become a no-op plus verification unless the user explicitly requests refresh/reapply.

## Failure modes and recovery

- Secret scan hit -> redact and flag.
- Evidence missing -> mark skipped; do not fabricate.


## Data contracts

Primary contracts: `operation-report, redaction-policy, consent-grant`. Any implementation-specific schema expansion MUST update `docs/planning/add-spicetify-skill/schemas/README.md`, `api-contracts.md`, and regression prompts.

## Cross-cutting controls

- Policy decision is required before execution, even for no-op verification plans.
- Secrets, prefs content, logs, screenshots, and private paths follow `privacy-redaction.md`.
- Third-party, Marketplace, imported, or unknown assets require provenance and audit before enablement.
- Desired-state or automation inputs cannot waive non-negotiable safety invariants.

## Example user prompts

- `/spicetify generate a report I can paste into a GitHub issue`

## Example structured response

```json
{
  "mode": "report",
  "type": "doctor",
  "redacted": true,
  "files": [
    "reports/doctor-20260607.md"
  ]
}
```

## Privacy reference

Use `../privacy-redaction.md` for redaction, evidence collection, retention, and report-sharing boundaries.
