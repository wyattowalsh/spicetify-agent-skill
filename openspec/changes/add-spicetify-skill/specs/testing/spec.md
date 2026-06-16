# Delta spec: testing

**Path:** `openspec/changes/add-spicetify-skill/specs/testing/spec.md`
**Purpose:** Behavior-level delta requirements for tests, fixtures, and CI safety.
**Status:** Proposed

## ADDED Requirements

### Requirement: Fake Spicetify CI
The system SHALL test command, state, config, repair, and rollback behavior against fake Spicetify environments rather than real Spotify.

#### Scenario: CI repair test
- GIVEN repair integration tests run in CI
- WHEN Spicetify commands are invoked
- THEN the fake binary records argv and simulates output
- AND no real Spotify path is touched

### Requirement: Live-Mutation Guard
The system SHALL fail tests if a command attempts to mutate real user Spicetify or Spotify paths.

#### Scenario: Real userdata path appears in CI
- GIVEN an integration test resolves a real home Spicetify path
- WHEN the guard evaluates the path
- THEN the test fails before mutation

### Requirement: Fixture Coverage
The system SHALL include fixtures for healthy state, broken state, platform-specific issues, malicious code, and rollback scenarios.

#### Scenario: Malicious extension fixture
- GIVEN an extension fixture combines token access and external network send
- WHEN audit tests run
- THEN the verdict is `block`

### Requirement: Story-Level Acceptance Coverage
The test plan MUST map each primary user story to modes, specs, schemas, fake fixtures, and done evidence.

#### Scenario: Reviewer checks MVP completeness
- GIVEN a reviewer wants to know whether the MVP is ready
- WHEN they inspect the acceptance matrix and validation outputs
- THEN every included user story has a passing happy path, blocked path, verification path, and rollback/report path

### Requirement: Deterministic Skill Eval Contracts
The system SHALL provide local deterministic evals that validate skill activation, mode routing, fixture-backed state, trace order, report schemas, artifacts, redaction, and fake-only execution without hosted providers or real Spicetify access.

#### Scenario: Eval suite proves behavior with fake fixtures
- GIVEN the local skill eval suite runs in strict mode
- WHEN a case references a missing fixture, emits an invalid trace, leaks a synthetic secret, or claims an unproduced report artifact
- THEN the eval run fails before acceptance
- AND fake execution cases run only through the approved fake Spicetify gate
