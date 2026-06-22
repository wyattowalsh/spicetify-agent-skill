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
- WHEN a case references a missing fixture, emits an invalid trace, leaks a synthetic secret, or claims an unplanned report artifact
- THEN the eval run fails before acceptance
- AND fake execution cases run only through the approved fake Spicetify gate

#### Scenario: Prompt-first routing eval
- GIVEN a prompt asks `/spicetify` to find, compare, audit, install, create, repair, debug, or evolve
- WHEN the deterministic eval runner grades the case
- THEN it checks the inferred primary intent, asset kind, source kind, next artifact, policy, state, trace, reports, and forbidden actions
- AND ambiguous or malicious prompts cannot produce mutating execution

#### Scenario: Existing asset research eval
- GIVEN a prompt asks for existing Spicetify plugins, extensions, themes, custom apps, snippets, or Marketplace items
- WHEN the eval runner grades the response
- THEN the report is read-only and distinguishes compatibility, maintenance, popularity, provenance readiness, and safety
- AND no candidate is treated as trusted or safe to install before staging, audit, provenance lock, dry-run plan, snapshot, confirmation, verification, and rollback metadata

### Requirement: Repository Quality Automation
The repository SHALL provide local hooks and GitHub Actions workflows that run the fake-only validation gates for runtime, skill payload, docs, evals, packaging, and OpenSpec without live Spotify or Spicetify access.

#### Scenario: Pull request validation
- GIVEN a pull request or push targets `main`
- WHEN the CI workflow runs
- THEN Python tests, Ruff, `ty`, bundle validation, generated-reference checks, eval suites, docs checks, package smoke checks, skill discovery, and OpenSpec validation run with fake Spicetify enabled and real Spicetify disabled

#### Scenario: Release tag validation
- GIVEN a `v*` tag is pushed
- WHEN the release verification workflow runs
- THEN the tag is checked against the package version
- AND the pinned `npx skills add github:<owner>/<repo>@<tag> --skill spicetify --list` path is verified
- AND no package publishing, docs deployment, real Spicetify execution, or official Spicetify bundling occurs

#### Scenario: Pinned docs package manager
- GIVEN a workflow installs docs dependencies
- WHEN Node setup completes
- THEN the workflow activates the package-manager version pinned in `package.json`
- AND it does not use setup-node pnpm caching before pnpm activation

#### Scenario: Local hook validation
- GIVEN a maintainer installs the local pre-commit hooks
- WHEN pre-commit and pre-push hooks run
- THEN fast formatting, lint, bundle, Python, docs, and eval gates execute through repo-owned validation commands
- AND the hooks do not mutate lockfiles, install dependencies, or access live Spotify/Spicetify state
