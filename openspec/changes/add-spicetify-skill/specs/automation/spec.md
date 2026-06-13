# Delta spec: automation

**Path:** `openspec/changes/add-spicetify-skill/specs/automation/spec.md`
**Purpose:** Requirements for power-user batch operations, manifests, headless use, and CI guardrails.
**Status:** Proposed
**Load/use when:** Implementing automation presets, batch mode, or CI checks.

## ADDED Requirements

### Requirement: Batch Plans Remain Transactional
The system SHALL represent multi-step automation as a batch of individually verifiable, rollbackable operation plans.

#### Scenario: Apply profile and install generated theme
- GIVEN a batch request includes profile switching and generated theme installation
- WHEN the batch plan is built
- THEN each mutation has its own policy decision, snapshot dependency, verification checks, and rollback pointer
- AND execution stops at the first failed required verification

### Requirement: Headless Mode Cannot Expand Authority
The system SHALL support structured headless dry-runs while preserving the same blocked actions and confirmation requirements as interactive mode.

#### Scenario: CI dry-run imports manifest
- GIVEN a CI job dry-runs a desired-state manifest
- WHEN the manifest includes third-party code and package scripts
- THEN the CI job reports required approvals
- AND does not download, install, build, or enable the assets

### Requirement: Automation Policy Is Explicit
The system SHALL allow power users to define policy presets only within the bounds of non-waivable safety invariants.

#### Scenario: Power user allows generated theme writes
- GIVEN a local policy preset allows generated theme writes under the Spicetify themes root
- WHEN the plan writes a new generated theme folder
- THEN the policy may classify it as low or medium risk according to configured thresholds
- AND it still requires path validation, snapshot policy, and verification
