# Delta spec: docs-site

**Path:** `openspec/changes/add-spicetify-skill/specs/docs-site/spec.md`
**Purpose:** Behavior requirements for the accompanying Fumadocs documentation site.
**Status:** Proposed

## ADDED Requirements

### Requirement: Accompanying Documentation Site
The system SHALL include a plan for an accompanying Fumadocs documentation site that presents `/spicetify` behavior, safety boundaries, workflows, schemas, and implementation guidance without replacing OpenSpec as the source of truth.

#### Scenario: Reviewer finds source of truth
- GIVEN a reviewer starts from the docs site plan
- WHEN they need authoritative behavior
- THEN the docs site SHALL link back to OpenSpec proposal, specs, design, tasks, schemas, and planning docs
- AND SHALL label generated documentation as derived from local source files.

#### Scenario: Site plan remains approval-gated
- GIVEN the docs site requires package installation or deployment
- WHEN a coding agent reaches that step
- THEN the plan MUST present commands as proposed commands
- AND MUST stop for explicit approval before installation, deployment, analytics, hosted search, or external registry changes.

### Requirement: Independent Docs App Boundary
The system SHALL plan the docs site as an independently buildable app with an explicit root, content root, validation commands, and rollback scope.

#### Scenario: Docs app rollback
- GIVEN docs-site implementation fails validation
- WHEN rollback is requested
- THEN rollback SHALL be scoped to the approved docs app root and related workspace metadata
- AND SHALL NOT delete unrelated project files or local `/spicetify` runtime state.
