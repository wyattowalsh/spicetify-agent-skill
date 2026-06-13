# Delta spec: docs-content

**Path:** `openspec/changes/add-spicetify-skill/specs/docs-content/spec.md`
**Purpose:** Behavior requirements for Fumadocs content architecture and generated references.
**Status:** Proposed

## ADDED Requirements

### Requirement: Progressive Docs Content
The system SHALL organize documentation content using progressive disclosure for novices, power users, implementers, and security reviewers.

#### Scenario: Novice reads quickstart
- GIVEN a novice opens the docs site
- WHEN they read the quickstart
- THEN the content SHALL explain dry-run-first behavior, snapshots, confirmations, and rollback before any mutating example.

#### Scenario: Implementer reads references
- GIVEN an implementer needs schema or mode details
- WHEN they open reference pages
- THEN the pages SHALL link to source schemas, OpenSpec requirements, mode docs, and validation rules.

### Requirement: Generated Content Provenance
The system SHALL make generated docs deterministic, source-linked, and reviewable.

#### Scenario: Generated schema page
- GIVEN a schema reference page is generated
- WHEN it is written to the docs content tree
- THEN it MUST include the source path, generation status, and validation status
- AND MUST NOT include secrets, private paths, or unresolved placeholders.

### Requirement: AI-Readable Documentation
The system SHALL plan AI-readable documentation routes that expose stable public docs content without leaking sensitive evidence.

#### Scenario: LLM route excludes private data
- GIVEN `llms.txt` or full AI-readable docs are generated
- WHEN report, log, screenshot, or local-run evidence exists
- THEN the generated AI-readable content MUST omit or redact that evidence according to the redaction policy.
