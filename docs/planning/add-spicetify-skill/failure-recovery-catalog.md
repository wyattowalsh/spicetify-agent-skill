# Failure recovery catalog

**Path:** `docs/planning/add-spicetify-skill/failure-recovery-catalog.md`
**Purpose:** Map known failure modes to detection signals, stop conditions, safe recovery, verification, and rollback behavior.
**Status:** Proposed
**Load/use when:** Implementing `doctor`, `repair`, `apply`, `rollback`, `report`, or test fixtures.

## Recovery posture

Recovery is staged, not heroic. The operator should preserve evidence, stop on unsafe uncertainty, and offer the smallest reversible repair before broader reset paths.

## Catalog

| Failure mode | Detection signal | Immediate stop? | Safe recovery plan | Verification | Rollback / fallback |
|---|---|---:|---|---|---|
| Spicetify binary missing | `ENOENT` or no version output from identity probe | Yes for mutation | Report install/manual setup options only; do not install automatically | no mutation occurred | none |
| Config path unavailable | `spicetify -c` fails or path missing | Yes for mutation | Run read-only setup diagnostics; suggest `spicetify` no-arg only as a proposed action | config path discovered or report explains block | none |
| Config parse failure | INI parser error or missing required sections | Yes | Snapshot raw config if safe; generate repair report; do not apply | parser succeeds after manual/user-approved repair | restore pre-repair snapshot |
| Spotify updated and patch state broken | FAQ-compatible symptoms or apply/update failure after Spotify update | No, if snapshot possible | Doctor → snapshot → `backup` → `apply`; separate confirmation for `restore` → `backup` → `apply` fallback | CLI success, config/files exist, doctor no new high findings | restore `/spicetify` snapshot; optional `spicetify restore` only if confirmed |
| Unsupported new Spotify build | CLI output or issue-tracker/manual evidence indicates unsupported build | Yes | Stop and report compatibility uncertainty; preserve current snapshot | no further mutation | rollback to last-known-good if requested |
| Missing theme file | config theme points to folder without `color.ini` or `user.css` | No, unless applying | Offer switch to known-good theme or restore snapshot | current theme files present and scheme valid | previous theme config |
| Theme collision | target theme name exists in user or executable theme roots | Yes for overwrite | Backup and require explicit overwrite/rename decision | hashes and precedence match plan | restore backup and prior config |
| Extension syntax/audit failure | parser/auditor finds JS syntax error, eval, token+network, or obfuscation | Yes for enable | Block enable; produce audit report; allow local edit/re-audit loop | audit verdict allow/warn with accepted risk | no enablement performed |
| Custom app manifest invalid | missing `index.js`, `manifest.json`, `active-icon`, bad paths/subfiles | Yes for enable | Block enable; provide precise manifest repairs | manifest parses and folder safe | no enablement performed |
| Marketplace installer requested | source asks for shell pipeline or external install script | Yes | Treat as manual-only; optionally audit repo/archive without running installer | no script executed | none |
| Path traversal/symlink escape | staged archive path escapes staging or symlink leaves allowed root | Yes | Quarantine staging dir; report blocked files | staging cleaned or quarantined | none |
| Permission/package manager required | AUR/APT/Flatpak chmod, Snap migration, package install/remove | Yes | Manual checklist; do not run `sudo`, `chmod`, package manager, or removal | user confirms manual remediation and re-runs doctor | none |
| DevTools/launch flag risk | remote debugging, log path, username/password flag, update endpoint override | Yes without consent | Require scoped consent, risk copy, rollback plan, redaction | flags match approved plan; logs redacted | restore prior launch flags/config |
| Plan drift after confirmation | plan hash/source/config/snapshot mismatch before execution | Yes | Invalidate confirmation and produce new dry-run | new plan hash approved | none |
| Verification failure after mutation | apply succeeds but config/files/audit/doctor checks fail | No, but pause | Auto-rollback if policy says fail-safe; otherwise stop with evidence | rollback verified or user keeps debug state | pre-operation snapshot |
| Rollback failure | snapshot hash mismatch, missing file, write error | Yes | Stop, preserve run log, generate manual recovery report | no further mutation | escalate to manual restore from preserved snapshot copy |
| Redaction failure | report/log contains token-like or prefs content after redaction pass | Yes for share/export | Block shareable report; keep local-only report if safe | secret scan passes | delete generated report if requested |
| Watch loop runaway | watcher exceeds duration, output limit, or repeated failures | Yes | Stop watcher, summarize last errors, keep files unchanged unless plan allowed writes | process stopped and temp files cleaned | restore temporary config if used |

## Recovery report minimum

Every failed mutating operation MUST report:

- failed step ID and mode;
- last completed safe checkpoint;
- snapshot ID or reason snapshot was unavailable;
- whether rollback was attempted;
- verification evidence;
- safe next actions;
- actions explicitly not taken because they require approval.

## Fixture requirements

Create one fixture per catalog row where practical. Each fixture should assert both the failure classification and the absence of prohibited side effects.
