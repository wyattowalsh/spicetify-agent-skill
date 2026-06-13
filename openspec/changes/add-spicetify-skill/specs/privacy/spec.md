# Delta spec: privacy

**Path:** `openspec/changes/add-spicetify-skill/specs/privacy/spec.md`
**Purpose:** Requirements for secret-safe evidence handling, redaction, snapshots, logs, screenshots, and reports.
**Status:** Proposed
**Load/use when:** Implementing report writing, DevTools evidence, snapshots, or diagnostics.

## ADDED Requirements

### Requirement: Sensitive Data Minimization
The system SHALL minimize sensitive data collection for every inspection, snapshot, report, log, screenshot, and audit operation.

#### Scenario: Snapshot sees Spotify prefs
- GIVEN the discovered Spotify prefs file exists
- WHEN a snapshot plan is built
- THEN the plan records prefs metadata only by default
- AND the prefs content is excluded unless the user explicitly approves a bounded diagnostic capture

#### Scenario: Report includes absolute paths
- GIVEN a report may include local usernames or private directory names in paths
- WHEN strict redaction is selected
- THEN the report masks user-identifying path segments while preserving enough path shape for debugging

### Requirement: Redaction Before Persistence
The system SHALL redact token-like values, credential-like flags, cookies, authorization headers, and private local data before writing shareable reports.

#### Scenario: DevTools log contains token-like text
- GIVEN a console log line contains a token-like value
- WHEN the report writer stores the log evidence
- THEN the stored report replaces the sensitive value with a stable redaction marker
- AND the report records that redaction occurred without exposing the original value

### Requirement: Evidence Consent
The system SHALL require explicit consent before collecting screenshots, DevTools logs, launch flags, or other high-context evidence.

#### Scenario: Optional screenshot verification requested
- GIVEN a mutating theme workflow can optionally collect a screenshot
- WHEN the user has not approved screenshot capture
- THEN the verifier skips screenshot capture
- AND reports the remaining non-visual checks that were run

### Requirement: Report Shareability
The system SHALL classify reports as local-only, redacted-shareable, or strict-shareable before presenting them as issue-ready output.

#### Scenario: User asks for a GitHub issue report
- GIVEN the report may include command output, file paths, and logs
- WHEN the user requests a shareable report
- THEN the system applies strict redaction
- AND runs a final secret-pattern check before writing or displaying the report
