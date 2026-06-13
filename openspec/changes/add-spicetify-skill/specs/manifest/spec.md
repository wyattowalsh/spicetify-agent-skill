# Delta spec: manifest

**Path:** `openspec/changes/add-spicetify-skill/specs/manifest/spec.md`
**Purpose:** Requirements for declarative desired-state manifests, profile automation, drift detection, and replay safety.
**Status:** Proposed
**Load/use when:** Implementing profile export/import, migration, repeatable setup, or power-user automation.

## ADDED Requirements

### Requirement: Desired State Manifest
The system SHALL support an stable desired-state manifest that declares config, profiles, assets, snippets, provenance locks, safety policy, and verification expectations.

#### Scenario: Export current setup
- GIVEN a user has a working local Spicetify setup
- WHEN the user requests export
- THEN the system creates a manifest that can be dry-run replayed
- AND the export separates generated/local/trusted assets from third-party assets

#### Scenario: Import manifest from another machine
- GIVEN a manifest references third-party assets not present locally
- WHEN the user requests import
- THEN the system builds a dry-run plan with missing assets, required provenance checks, and audit requirements
- AND it does not download or enable third-party code by default

### Requirement: Drift-Aware Replay
The system SHALL compare desired-state manifests against current local state and emit explicit no-op, add, remove, modify, audit, and approval steps.

#### Scenario: Manifest already matches local state
- GIVEN current config and assets match the manifest
- WHEN the user dry-runs the manifest
- THEN the plan contains no file/config mutations
- AND verification checks still run

#### Scenario: Manifest differs from local config
- GIVEN current config has extra enabled extensions
- WHEN the user dry-runs the manifest
- THEN the plan lists exact removals and additions
- AND destructive or third-party changes require confirmation before execution

### Requirement: Manifest Safety Overrides Are Limited
The system SHALL not allow manifests or automation presets to disable core safety invariants.

#### Scenario: Manifest disables snapshots
- GIVEN an imported manifest asks to skip snapshots for a medium-risk mutation
- WHEN the policy engine evaluates the plan
- THEN the system ignores or rejects the unsafe override
- AND explains the invariant that cannot be waived
