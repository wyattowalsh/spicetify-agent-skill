# Delta spec: customization

**Path:** `openspec/changes/add-spicetify-skill/specs/customization/spec.md`
**Purpose:** Behavior-level delta requirements for customization workflows.
**Status:** Proposed

## ADDED Requirements

### Requirement: Theme Workflow
The system SHALL create, validate, install, switch, and remove themes with backups and verification.

#### Scenario: Create terminal theme
- GIVEN the user requests a dark terminal-style theme
- WHEN the skill plans creation
- THEN the plan creates `color.ini` and `user.css`, validates them, snapshots, configures, applies, and verifies

#### Scenario: Existing theme collision
- GIVEN a target theme folder already exists
- WHEN the plan is built
- THEN overwrite requires backup and explicit confirmation

### Requirement: Extension and Custom App Workflow
The system SHALL scaffold, build, audit, install, enable, debug, disable, and remove extensions and custom apps through typed flows.

#### Scenario: Scaffold extension
- GIVEN the user asks for a TypeScript React extension
- WHEN the skill plans scaffolding
- THEN the plan uses a maintained bundler template
- AND avoids third-party install scripts by default

#### Scenario: Enable custom app
- GIVEN a custom app folder is staged
- WHEN the user asks to enable it
- THEN the plan validates manifest and `index.js`, audits code, snapshots, configures, applies, and verifies

### Requirement: Snippet and Marketplace Workflow
The system SHALL treat snippets and Marketplace assets as customization sources that require provenance and audit before local mutation.

#### Scenario: Install Marketplace theme safely
- GIVEN a GitHub theme source is provided
- WHEN the skill plans installation
- THEN the plan stages, audits, snapshots, copies, applies, and verifies rather than running install scripts

#### Scenario: Research existing Marketplace assets
- GIVEN the user asks `/spicetify` to find or compare existing Marketplace themes, extensions, custom apps, or snippets
- WHEN the skill researches candidates
- THEN it produces a read-only asset analysis report with compatibility, maintenance, risk, provenance readiness, confidence, and recommended next action
- AND it never calls a candidate trusted, safe to install, or installed from research metadata alone

#### Scenario: Existing asset advances to install planning
- GIVEN a user selects a researched third-party asset for possible installation
- WHEN the skill builds the next plan
- THEN explicit approval, immutable source pinning, temp staging, path guards, file hashes, inspection, audit, and provenance lock are required before any dry-run install plan

### Requirement: Creator Compatibility Boundary
The system SHALL treat Spicetify Creator as a compatibility path rather than the default scaffold generator.

#### Scenario: User requests Creator project
- GIVEN the user explicitly requests Spicetify Creator compatibility
- WHEN the skill plans scaffolding
- THEN the plan explains deprecation risk
- AND requires approval before package scripts are run
