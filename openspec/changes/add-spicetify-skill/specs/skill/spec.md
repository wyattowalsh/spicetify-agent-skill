# Delta spec: skill

**Path:** `openspec/changes/add-spicetify-skill/specs/skill/spec.md`
**Purpose:** Behavior-level delta requirements for `skill`.
**Status:** Proposed

## ADDED Requirements

### Requirement: Skill Invocation
The system SHALL expose a single user-facing skill invocation named `/spicetify`.

#### Scenario: Route semantic mode prompt
- GIVEN a user prompt begins with `/spicetify` and requests a Spicetify workflow
- WHEN the skill classifies the request
- THEN the response identifies the selected mode
- AND produces a dry-run plan when mutation is possible

#### Scenario: Avoid alternate surface names
- GIVEN the user asks for Spicetify workflow help
- WHEN the skill presents its identity
- THEN the visible skill name is `/spicetify`

### Requirement: Progressive Disclosure
The system SHALL reveal the smallest sufficient context for the user's current decision.

#### Scenario: Brief response for read-only question
- GIVEN the user asks where config lives
- WHEN no mutation is requested
- THEN the skill answers briefly
- AND points to deeper docs only when useful

#### Scenario: Deep plan for implementation handoff
- GIVEN the user asks for a coding-agent handoff
- WHEN the request is production-grade
- THEN the skill references OpenSpec, tasks, Goal, PLANS, validation, and stop rules without embedding all documents inline

### Requirement: Mode Routing
The system SHALL route supported intents to semantic modes rather than raw command passthrough.

#### Scenario: Repair intent
- GIVEN the user says Spotify updated and Spicetify broke
- WHEN the skill routes the request
- THEN the selected mode is `repair`
- AND doctor and snapshot prerequisites are included

#### Scenario: Audit intent
- GIVEN the user asks whether an extension is safe
- WHEN the skill routes the request
- THEN the selected mode is `audit`
- AND no code is executed
