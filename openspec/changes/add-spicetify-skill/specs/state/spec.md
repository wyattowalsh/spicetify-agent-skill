# Delta spec: state

**Path:** `openspec/changes/add-spicetify-skill/specs/state/spec.md`
**Purpose:** Behavior-level delta requirements for `state`.
**Status:** Proposed

## ADDED Requirements

### Requirement: Snapshot Before Mutation
The system SHALL create or require a valid snapshot before any medium- or high-risk mutation.

#### Scenario: Theme switch snapshot
- GIVEN a user switches themes
- WHEN the plan is approved
- THEN a config/assets snapshot is created before config or file changes

#### Scenario: Snapshot failure
- GIVEN snapshot creation fails
- WHEN the user requests apply
- THEN execution stops before mutation

### Requirement: Last Known Good
The system SHALL update last-known-good only after post-operation verification succeeds.

#### Scenario: Successful apply
- GIVEN a mutating operation succeeds and verifies
- WHEN the run completes
- THEN last-known-good points to the new verified snapshot

#### Scenario: Failed verification
- GIVEN an operation exits zero but verification fails
- WHEN the run completes
- THEN last-known-good remains unchanged

### Requirement: Rollback
The system SHALL restore from a validated snapshot and verify the restored state.

#### Scenario: Rollback current state
- GIVEN a user asks to roll back
- WHEN a target snapshot is selected
- THEN the system creates a pre-rollback snapshot and restores files/config from the target

### Requirement: Snapshot Exclusions
The system SHALL exclude sensitive or non-restorable data from snapshots by default.

#### Scenario: Spotify prefs exists
- GIVEN the user has a Spotify prefs file
- WHEN a snapshot is created
- THEN prefs content is excluded
- AND only redacted metadata may be stored when needed for diagnostics

### Requirement: Single Writer Operation Lock
The system MUST prevent overlapping mutating operations against the same discovered Spicetify userdata or config roots.

#### Scenario: Concurrent profile switch
- GIVEN one approved mutating operation is executing for a Spicetify userdata root
- WHEN another mutating operation targets the same root
- THEN the second operation is stopped before snapshot or mutation
- AND the report identifies the active operation lock and safe retry path

#### Scenario: Concurrent apply is blocked
- GIVEN a mutating `/spicetify` operation is running for a userdata root
- WHEN another mutating operation targets the same root
- THEN the system refuses or queues the second operation before mutation
- AND reports the active run ID and safe recovery option

### Requirement: Confirmation Drift Tracking
The system MUST record the plan hash used at execution and whether drift checks matched, invalidated, or required manual reconfirmation.

#### Scenario: Plan hash mismatch at execution
- GIVEN an operation run references a confirmation grant
- WHEN the run-time plan hash differs from the confirmed plan hash
- THEN execution stops before mutation
- AND the run report records `drifted-invalidated`
