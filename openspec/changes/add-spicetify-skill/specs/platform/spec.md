# Delta spec: platform

**Path:** `openspec/changes/add-spicetify-skill/specs/platform/spec.md`
**Purpose:** Behavior-level delta requirements for platform/package detection and stop rules.
**Status:** Proposed

## ADDED Requirements

### Requirement: Platform Discovery
The system SHALL discover paths and package-specific constraints through read-only probes before proposing mutation.

#### Scenario: Prefer CLI path probes
- GIVEN Spicetify is available
- WHEN inspect runs
- THEN it uses `spicetify -c` and `spicetify path` before applying platform defaults

### Requirement: Unsupported Package Stop
The system SHALL stop mutation when the detected Spotify package cannot be safely modified by Spicetify.

#### Scenario: Linux Snap Spotify
- GIVEN doctor detects Snap Spotify
- WHEN repair is requested
- THEN the plan is blocked for mutation
- AND a manual migration note is reported instead of running package commands

### Requirement: Permission Change Approval
The system SHALL not execute permission changes automatically.

#### Scenario: APT Spotify needs writable app directory
- GIVEN doctor detects a permission issue under `/usr/share/spotify`
- WHEN repair is planned
- THEN the plan stops with manual instructions
- AND does not run `sudo`, `chmod`, or ownership changes

### Requirement: Declarative Ownership Warning
The system SHALL warn before mutating state that appears managed by a declarative system.

#### Scenario: Nix-managed Spicetify
- GIVEN inspect finds Nix or Home Manager ownership markers
- WHEN a profile or theme mutation is requested
- THEN the plan recommends export/manifest mode unless the target path is explicitly approved

### Requirement: Declarative System Preservation
The system SHALL avoid mutating paths that appear owned by declarative package or profile systems unless explicitly approved.

#### Scenario: Home Manager owns profile
- GIVEN inspect detects that Spicetify state appears managed declaratively
- WHEN the user requests a local profile switch
- THEN the plan recommends export or declarative-manifest guidance
- AND no local mutation occurs without explicit target-path approval
