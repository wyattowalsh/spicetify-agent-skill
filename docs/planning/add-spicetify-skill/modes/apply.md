# Mode: apply

**Path:** `docs/planning/add-spicetify-skill/modes/apply.md`
**Purpose:** Detailed contract for `/spicetify apply` mode.
**Status:** Proposed
**Load/use when:** Implementing, testing, or reviewing `apply` behavior.

## Purpose

Execute an approved dry-run plan exactly as reviewed.

## Inputs

`planId`, `confirmationToken`, `allowAutoRollback?`.

## Preconditions

Plan exists, hash matches token, policy permits execution, snapshot requirement satisfied.

## Commands/files touched

Exactly planned commands/files/state pointers.

## Safety checks

No new commands/mutations at execution time; drift blocks; rollback plan must exist for mutation.

## Plan output

`ApplyPlan` is usually an execution request referencing an existing `OperationPlan`.

## Execution flow

Validate token; snapshot; execute steps; verify each checkpoint; report.

## Verification flow

Required verifiers for mode plus no new high-severity doctor findings.

## Rollback flow

Automatic or offered rollback from pre-apply snapshot on verification failure.

## Idempotency notes

The planner MUST diff current state before emitting mutations. Re-running an already satisfied desired state SHOULD become a no-op plus verification unless the user explicitly requests refresh/reapply.

## Failure modes and recovery

- Plan drift -> block execution and emit new diff.
- Verification failure -> recommend rollback; do not update last-known-good.


## Data contracts

Primary contracts: `operation-plan, policy-decision, operation-run`. Any implementation-specific schema expansion MUST update `docs/planning/add-spicetify-skill/schemas/README.md`, `api-contracts.md`, and regression prompts.

## Cross-cutting controls

- Policy decision is required before execution, even for no-op verification plans.
- Secrets, prefs content, logs, screenshots, and private paths follow `privacy-redaction.md`.
- Third-party, Marketplace, imported, or unknown assets require provenance and audit before enablement.
- Desired-state or automation inputs cannot waive non-negotiable safety invariants.

## Example user prompts

- `/spicetify apply plan_123 after showing me the diff`

## Example structured response

```json
{
  "mode": "apply",
  "planId": "plan_123",
  "snapshotId": "snap_456",
  "status": "verified"
}
```

## Confirmation reference

Use `../confirmation-flow.md` whenever this mode crosses snapshot, mutation, destructive, third-party-code, DevTools, network, package-manager, permission, or launch-flag approval gates.
