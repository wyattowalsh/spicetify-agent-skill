# Mode: uninstall

**Path:** `docs/planning/add-spicetify-skill/modes/uninstall.md`
**Purpose:** Detailed contract for `/spicetify uninstall` mode.
**Status:** Proposed
**Load/use when:** Implementing, testing, or reviewing `uninstall` behavior.

## Purpose

Safely remove skill-managed assets or produce manual full-uninstall plans.

## Inputs

`scope`, asset ID, `deleteFiles?`, `restoreVanilla?`.

## Preconditions

Snapshot and ownership/provenance known for deletions.

## Commands/files touched

Config removals, skill-owned file deletes, optional `spicetify restore` with high-risk confirmation.

## Safety checks

No package-manager uninstall; exact manifest for recursive deletion; confirmation for every delete.

## Plan output

`UninstallPlan` with disable/remove/delete/restore steps, backups, rollback.

## Execution flow

Snapshot → disable config → apply/restore if approved → delete skill-owned files if approved.

## Verification flow

Config no longer references removed items; deleted files match plan only.

## Rollback flow

Restore pre-uninstall snapshot.

## Idempotency notes

The planner MUST diff current state before emitting mutations. Re-running an already satisfied desired state SHOULD become a no-op plus verification unless the user explicitly requests refresh/reapply.

## Failure modes and recovery

- Non-skill-owned delete -> require explicit selection.
- Full uninstall -> manual checklist unless separately confirmed.


## Data contracts

Primary contracts: `operation-plan, snapshot-manifest, policy-decision`. Any implementation-specific schema expansion MUST update `docs/planning/add-spicetify-skill/schemas/README.md`, `api-contracts.md`, and regression prompts.

## Cross-cutting controls

- Policy decision is required before execution, even for no-op verification plans.
- Secrets, prefs content, logs, screenshots, and private paths follow `privacy-redaction.md`.
- Third-party, Marketplace, imported, or unknown assets require provenance and audit before enablement.
- Desired-state or automation inputs cannot waive non-negotiable safety invariants.

## Example user prompts

- `/spicetify uninstall the generated terminal theme`

## Example structured response

```json
{
  "mode": "uninstall",
  "scope": "theme",
  "deletes": 3,
  "requiresConfirmation": true
}
```

## Confirmation reference

Use `../confirmation-flow.md` whenever this mode crosses snapshot, mutation, destructive, third-party-code, DevTools, network, package-manager, permission, or launch-flag approval gates.
