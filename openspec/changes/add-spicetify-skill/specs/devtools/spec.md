# Delta spec: devtools

**Path:** `openspec/changes/add-spicetify-skill/specs/devtools/spec.md`
**Purpose:** Behavior-level delta requirements for debugging, logs, screenshots, and launch flags.
**Status:** Proposed

## ADDED Requirements

### Requirement: Debug Consent
The system SHALL require explicit consent before enabling DevTools, collecting console logs, capturing screenshots, or changing launch flags.

#### Scenario: Enable DevTools
- GIVEN a user asks to debug an extension
- WHEN the plan includes `spicetify enable-devtools`
- THEN the risk is high or medium according to policy
- AND confirmation is required before execution

### Requirement: Log Redaction
The system SHALL redact sensitive values before storing or sharing DevTools logs.

#### Scenario: Console includes token-like value
- GIVEN DevTools collection includes a token-like string
- WHEN the report is written
- THEN the token is masked
- AND the report records that redaction occurred

### Requirement: Bounded Debug Sessions
The system SHALL bound watch/log/screenshot sessions by duration, output size, and cancellation path.

#### Scenario: Watch mode starts
- GIVEN watch mode is approved
- WHEN the session starts
- THEN the report includes how to stop it
- AND log size and duration caps are enforced

### Requirement: Bounded Debug Evidence
The system SHALL collect DevTools logs, screenshots, and launch-flag evidence only within the approved duration, scope, and redaction policy.

#### Scenario: Console log collection requested
- GIVEN the user approves DevTools log collection for a fixed duration
- WHEN logs are collected
- THEN the report includes only redacted bounded evidence
- AND raw logs are not included in snapshots by default
