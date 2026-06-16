# Delta spec: skill

**Path:** `openspec/changes/add-spicetify-skill/specs/skill/spec.md`
**Purpose:** Behavior-level delta requirements for `skill`.
**Status:** Proposed

## ADDED Requirements

### Requirement: Skill Invocation
The system SHALL expose a single user-facing skill invocation named `/spicetify`.

#### Scenario: Route natural-language prompt
- GIVEN a user prompt begins with `/spicetify` and requests a Spicetify workflow
- WHEN the skill classifies the request
- THEN the response infers the safest route without requiring the user to choose a mode
- AND the response produces a read-only answer, research report, audit report, dry-run plan, clarification, or refusal
- AND mutation is never executed from the initial prompt

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
The system SHALL route supported natural-language prompts to internal semantic modes rather than raw command passthrough or user-selected mode requirements.

#### Scenario: Repair intent
- GIVEN the user says Spotify updated and Spicetify broke
- WHEN the skill routes the request
- THEN the inferred primary route is repair
- AND doctor and snapshot prerequisites are included

#### Scenario: Audit intent
- GIVEN the user asks whether an extension is safe
- WHEN the skill routes the request
- THEN the inferred route includes inspect and audit behavior
- AND no code is executed

#### Scenario: Research existing extension intent
- GIVEN the user asks `/spicetify` to find or compare existing extensions
- WHEN the skill routes the request
- THEN the inferred route produces a read-only research report
- AND Marketplace presence, GitHub topics, stars, and README claims are treated as discovery metadata rather than trust

#### Scenario: Unsafe shell intent
- GIVEN the user asks `/spicetify` to run a shell pipeline or README installer
- WHEN the skill routes the request
- THEN the route is refused or marked manual-only
- AND no shell command, package-manager command, installer script, or user argv passthrough is emitted
