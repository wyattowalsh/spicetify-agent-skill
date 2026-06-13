# Workflow: state, snapshots, restore, and rollback

**Path:** `docs/planning/add-spicetify-skill/workflows/state-snapshots-rollback.md`
**Purpose:** Define transactional state handling and last-known-good semantics.
**Status:** Proposed
**Load/use when:** Implementing `SnapshotStore`, `TransactionRunner`, `restore`, `rollback`, or `apply`.

## Distinction from Spicetify backup

Spicetify backup protects vanilla Spotify patch state. `/spicetify` snapshots protect the user’s Spicetify configuration and customization assets. Both are useful; they are not interchangeable.

## Snapshot scope

Default capture:

- `config-xpui.ini`
- discovered `Themes/`, `Extensions/`, `CustomApps/`
- `/spicetify` profile manifests, provenance locks, operation reports
- redacted discovery outputs: Spicetify CLI identity string, config path, userdata path, Spotify path

Default exclusions:

- Spotify prefs content
- caches
- logs unless explicitly included and redacted
- symlink targets outside allowed roots
- secrets or token-like content

## Transaction phases

```text
idle
  -> planned
  -> preflight-ok
  -> operation-lock-acquired
  -> snapshot-created
  -> executing
  -> verifying
  -> verified -> last-known-good-updated
  -> failed -> rollback-available
  -> rolled-back | stopped-for-human
```

See `operation-state-machine.md` for the canonical state machine.

## Snapshot policy

- Snapshot before every medium/high mutation.
- Snapshot before restore/rollback/uninstall.
- Failed snapshot blocks execution.
- Snapshot manifests are immutable and hash every captured file.
- Last-known-good updates only after verification succeeds and doctor has no new high-severity findings.
- Snapshot creation must reject symlink escapes and files outside discovered/approved roots.

## Operation locking

- Mutating operations acquire a lock scoped to the discovered Spicetify userdata/config root.
- The lock records plan ID, process ID when available, start time, target roots, and recovery instructions.
- A stale lock can be cleared only after read-only verification and a recovery report.
- Read-only inspect/audit/report may proceed without the mutating lock unless they collect sensitive logs or screenshots.

## Drift handling

Before execution, `/spicetify` recomputes planned precondition hashes. If config/assets/source files changed since the plan was approved, execution stops with `PLAN_DRIFT_DETECTED` and emits a new dry-run diff.

## Restore vs rollback

- `restore`: restore a user-selected snapshot/scope.
- `rollback`: restore the plan’s pre-operation or last-known-good snapshot.
- `spicetify restore`: restore vanilla Spotify patch state; high-risk, separate confirmation.

## Recovery strategy

| Failure point | Recovery |
|---|---|
| Snapshot fails | No mutation; report exact failure. |
| File staging fails | Delete staging temp; no source mutation. |
| Config mutation fails | Restore config from snapshot; stop. |
| `apply` fails | Stop; offer rollback or debug-preserve. |
| Verification fails | Do not update last-known-good; recommend rollback. |
| Rollback fails | Emit manual restore instructions and preserve evidence. |
| Operation lock stale | Clear only after read-only process/root verification and report. |

## Regression tests

- Snapshot hashes match source files.
- Snapshot restore returns exact file hashes.
- Rollback after failed apply restores previous config.
- Last-known-good is not updated on partial verification.
- Symlink escapes are rejected.
- Concurrent mutating plans for the same root are rejected.
