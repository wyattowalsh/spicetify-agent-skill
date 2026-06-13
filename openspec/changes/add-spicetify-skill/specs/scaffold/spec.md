# Delta spec: scaffold

**Path:** `openspec/changes/add-spicetify-skill/specs/scaffold/spec.md`
**Purpose:** Requirements for local theme, extension, custom-app, and snippet scaffolding.
**Status:** Proposed
**Load/use when:** Implementing generated project templates and developer workflows.

## ADDED Requirements

### Requirement: Maintained Scaffold Templates
The system SHALL generate local maintained templates for TypeScript extension and custom-app development instead of relying on deprecated scaffolding tools as the default.

#### Scenario: User requests TypeScript React extension
- GIVEN the user asks to scaffold a TypeScript React Spicetify extension
- WHEN the scaffold plan is built
- THEN the plan uses the maintained `/spicetify` template
- AND marks package installation or build execution as a separate approval-gated action

### Requirement: Creator Compatibility Boundary
The system SHALL expose Spicetify Creator only as an explicit compatibility option with current-source warning and migration guidance.

#### Scenario: User asks for Creator project
- GIVEN official docs describe Creator workflows but the source repository marks Creator deprecated
- WHEN the user asks to use Creator
- THEN the plan explains the conflict
- AND asks for explicit acceptance before producing a Creator-compatible project plan

### Requirement: Scaffold Output Audit
The system SHALL audit generated build outputs before installation or enablement even when the source was generated locally.

#### Scenario: Generated extension build completed
- GIVEN a generated extension produced a bundled JavaScript file
- WHEN installation is requested
- THEN the audit engine checks the built file for blocked patterns
- AND the installer verifies the source-to-output hash relationship recorded in the operation report

### Requirement: Package Script Approval
The system SHALL not run package scripts from third-party or imported projects without explicit approval and source audit.

#### Scenario: Third-party custom app requires build script
- GIVEN a downloaded custom app requires a package script to build
- WHEN the user asks to install it safely
- THEN the system audits package metadata and source first
- AND emits a manual or confirmation-gated build plan rather than running the script automatically
