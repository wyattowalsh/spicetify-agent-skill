# Delta spec: repair

**Path:** `openspec/changes/add-spicetify-skill/specs/repair/spec.md`
**Purpose:** Behavior-level delta requirements for `repair`.
**Status:** Proposed

## ADDED Requirements

### Requirement: Doctor Diagnostics
The system SHALL diagnose Spicetify state through read-only probes before proposing repair.

#### Scenario: Broken update
- GIVEN the user reports Spotify updated and Spicetify broke
- WHEN doctor runs
- THEN the system checks CLI/client identity, config path, paths, assets, package-specific issues, and repair candidates

### Requirement: Post-Spotify-Update Repair
The system SHALL implement post-update repair as a staged, snapshot-protected plan with fallback confirmation gates.

#### Scenario: Safe repair
- GIVEN doctor indicates reapply is likely needed
- WHEN repair is planned
- THEN the plan snapshots then runs `spicetify backup` and `spicetify apply` with verification

#### Scenario: Fallback repair
- GIVEN backup/apply fails
- WHEN fallback is needed
- THEN `spicetify restore` → `backup` → `apply` is not executed without separate confirmation

### Requirement: Unsupported Spotify Build Handling
The system SHALL report unsupported Spotify/Spicetify compatibility states without pretending repair is guaranteed.

#### Scenario: Unsupported update suspected
- GIVEN CLI output or doctor evidence indicates the current Spotify build may not be supported
- WHEN repair is evaluated
- THEN mutation stops or is downgraded to manual guidance
- AND the report recommends checking upstream issue status
