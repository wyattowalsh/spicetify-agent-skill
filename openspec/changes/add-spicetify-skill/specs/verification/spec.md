# Delta spec: verification

**Path:** `openspec/changes/add-spicetify-skill/specs/verification/spec.md`
**Purpose:** Behavior-level delta requirements for `verification`.
**Status:** Proposed

## ADDED Requirements

### Requirement: Verification Loop
The system SHALL verify every mutating operation through command, config, filesystem, and optional visual/log checks.

#### Scenario: Theme apply verification
- GIVEN a theme operation completes
- WHEN verification runs
- THEN the system checks command status, config values, required files, and optional screenshots

#### Scenario: Extension debug verification
- GIVEN an extension is enabled
- WHEN verification runs
- THEN the system checks config, file existence, syntax parse, and optional redacted DevTools console

### Requirement: Structured Reports
The system SHALL produce redacted structured reports for operations, audits, errors, and diagnostics.

#### Scenario: Doctor report
- GIVEN doctor completes
- WHEN the user asks for a shareable report
- THEN the report redacts secrets and includes findings, evidence, next actions, and validation status

### Requirement: Verification Failure Recovery
The system SHALL provide safe recovery options when verification fails.

#### Scenario: Apply exits zero but file check fails
- GIVEN a command exits successfully
- WHEN required file verification fails
- THEN the operation is not marked verified
- AND rollback or manual inspection is offered
