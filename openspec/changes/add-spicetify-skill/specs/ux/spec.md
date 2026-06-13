# Delta spec: ux

**Path:** `openspec/changes/add-spicetify-skill/specs/ux/spec.md`
**Purpose:** Behavior-level delta requirements for novice and power-user UX.
**Status:** Proposed

## ADDED Requirements

### Requirement: Novice-Safe Explanations
The system SHALL explain risks and next actions in plain language for mutating or blocked workflows.

#### Scenario: Blocked install script
- GIVEN a novice asks to install a GitHub theme using its README script
- WHEN policy blocks the script
- THEN the response explains why
- AND offers a safe staged audit workflow

### Requirement: Power-User Structured Output
The system SHALL provide structured JSON-compatible plans and reports for automation-oriented users.

#### Scenario: Profile dry-run
- GIVEN a power user requests profile switching
- WHEN the dry-run is built
- THEN the response includes a structured diff of config, assets, commands, verification, and rollback

### Requirement: Confirmation Clarity
The system SHALL name every destructive or high-risk effect before requesting confirmation.

#### Scenario: Uninstall skill-owned theme
- GIVEN uninstall will delete files
- WHEN confirmation is requested
- THEN the exact files and backup snapshot are shown
