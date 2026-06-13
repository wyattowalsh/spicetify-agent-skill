# Workflow: verification

**Path:** `docs/planning/add-spicetify-skill/workflows/verification.md`
**Purpose:** Define how `/spicetify` proves that operations succeeded and remains rollbackable.
**Status:** Proposed
**Load/use when:** Implementing `Verifier`, operation reports, and last-known-good updates.

## Verification contract

A mutating operation is successful only when all required checks pass:

- executed commands match the approved plan
- exit codes and parsed output are acceptable
- config parses and matches desired diff
- required files exist and hashes match
- audit/provenance decisions are still valid
- doctor reports no new high-severity findings
- rollback path remains available

## Evidence channels

| Channel | Required? | Notes |
|---|---:|---|
| CLI output | yes for CLI steps | Redact before storing/reporting. |
| Config parse/diff | yes for config/profile/theme/extension/custom-app | Exact-state compare for profiles. |
| Filesystem hashes | yes for file writes/copies | Compare planned hashes after transaction. |
| Snapshot manifest | yes for mutating plans | Verify snapshot integrity before mutation. |
| Audit report | yes for third-party/generated code | Check content hash has not drifted. |
| Doctor post-check | yes for apply/repair/rollback | No new high findings. |
| Screenshot | optional | User-approved visual evidence only. |
| DevTools logs | optional | User-approved, bounded, redacted. |

## Last-known-good rules

Update last-known-good only when:

1. plan finished successfully,
2. required verification passed,
3. no rollback was needed,
4. no new high severity doctor finding exists,
5. the report was written.

## Failure classification

- `verification_failed_config`: config mismatch or parse error.
- `verification_failed_filesystem`: missing/mismatched files.
- `verification_failed_cli`: command failure or known bad stderr.
- `verification_failed_audit_drift`: content hash differs from accepted audit.
- `verification_failed_doctor`: new high-severity finding.
- `verification_skipped_optional`: optional screenshot/log check skipped.

## Regression tests

- failed verification does not update last-known-good.
- optional screenshot/log skipping is not a failure.
- audit hash drift blocks third-party enablement.
- verification report validates against schema.
