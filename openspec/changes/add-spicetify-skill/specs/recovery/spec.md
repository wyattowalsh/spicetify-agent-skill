# Delta spec: recovery

**Path:** `openspec/changes/add-spicetify-skill/specs/recovery/spec.md`
**Purpose:** OpenSpec delta requirements for failure classification and recovery behavior.
**Status:** Proposed

## ADDED Requirements

### Requirement: Failure Classification
The system MUST classify failed operations into a stable error category with severity, failed step, evidence, snapshot availability, and safe next actions.

#### Scenario: Apply verification fails
- GIVEN a mutating apply run has executed at least one mutation
- WHEN post-apply verification fails
- THEN the system reports the failed verification step, prior checkpoint, available snapshot, and rollback recommendation
- AND it does not update last-known-good.

### Requirement: Recovery Catalog
The system MUST map known Spicetify, filesystem, platform, audit, privacy, and verification failures to predefined stop, retry, rollback, or manual-only recovery strategies.

#### Scenario: Platform permission repair requires elevated action
- GIVEN doctor detects that a repair would require package-manager or permission-changing commands
- WHEN the user asks `/spicetify` to fix it automatically
- THEN the system marks the recovery as manual-only
- AND it does not execute package-manager, permission, or installer commands.

### Requirement: Fail-Safe Rollback
The system MUST attempt rollback only when the operation plan defines a safe rollback path and the snapshot manifest validates.

#### Scenario: Snapshot hash mismatch prevents rollback
- GIVEN an operation fails after mutation
- AND the referenced snapshot manifest hash check fails
- WHEN rollback is requested
- THEN the system stops before overwriting files
- AND reports manual recovery steps and preserved evidence.

### Requirement: Recovery Report Completeness
The system MUST produce a recovery report whenever a mutating operation stops, fails, or rolls back.

#### Scenario: Repair fallback requires separate confirmation
- GIVEN Spotify-update repair completed doctor and snapshot
- WHEN primary backup/apply fails and the fallback would run restore/backup/apply
- THEN the system reports the fallback as high-risk and separately confirmable
- AND includes the snapshot ID, failed command evidence, and safe next actions.
