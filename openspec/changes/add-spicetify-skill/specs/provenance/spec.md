# Delta spec: provenance

**Path:** `openspec/changes/add-spicetify-skill/specs/provenance/spec.md`
**Purpose:** Behavior-level delta requirements for source provenance and lockfiles.
**Status:** Proposed

## ADDED Requirements

### Requirement: Source Provenance Lock
The system SHALL record source kind, source ref, file hashes, audit ID, verdict, and accepted risk before installing third-party assets.

#### Scenario: GitHub theme staged
- GIVEN a theme is downloaded from GitHub
- WHEN installation is approved
- THEN the lockfile records the repository, ref, file hashes, audit verdict, and install target

### Requirement: Audit Invalidation On Drift
The system SHALL invalidate prior audit acceptance when source files change.

#### Scenario: Staged file hash changes
- GIVEN an extension was audited
- WHEN its staged file hash changes before enablement
- THEN the previous audit acceptance is invalid
- AND execution stops until a new audit is accepted

### Requirement: Marketplace Metadata Is Not Trust
The system SHALL not treat Marketplace-compatible metadata as proof of code safety.

#### Scenario: Valid Marketplace manifest with risky JS
- GIVEN a repository has valid Marketplace tags and manifest
- WHEN its extension code contains blocked patterns
- THEN the audit verdict remains `block`
