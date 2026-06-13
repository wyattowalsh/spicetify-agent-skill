# Validation: `/spicetify`

**Path:** `docs/planning/add-spicetify-skill/validation.md`
**Purpose:** Validation matrix and acceptance checks for the planning bundle and implementation.
**Status:** Active validation matrix for the safe MVP and remaining workflow tasks
**Load/use when:** Running checks before handoff or implementation completion.

## Planning-bundle validation

```bash
python tools/validate_bundle.py --root .
python -m json.tool evals/regression-prompts.json >/dev/null
python - <<'PY'
from pathlib import Path
import json
for p in Path('schemas').glob('*.json'):
    json.load(open(p))
print('schemas ok')
PY
```

Expected result: no errors. Warnings must be triaged in the audit report.

If the host does not provide `python`, record the literal command failure and run the equivalent command with `python3` when available. Keep those statuses separate so an interpreter alias issue is not confused with a bundle validation failure.

## OpenSpec validation

```bash
openspec validate add-spicetify-skill --strict
openspec validate --all --strict
```

Run in a target repo with OpenSpec installed. If OpenSpec is unavailable, document that the command was not run and keep the artifact-level validator result separate.

In this repo on 2026-06-13, the global `openspec` command was not available on PATH. After explicit approval, equivalent strict checks passed through `npx --package @fission-ai/openspec@1.4.1 openspec ...`.

## Implementation validation matrix

| Area | Required checks |
|---|---|
| Command registry | allowed verbs, rejected unknown args, `shell:false`, no combined command shortcuts. |
| Policy | read/low/medium/high/manual/block paths, confirmation hash drift, blocked shell/script prompts. |
| Plan execution | plan hash/policy recomputation, command registry revalidation, snapshot-before-command, and rejection of mutating no-command plans except explicit snapshot-only runs. |
| Snapshot | immutable manifests, hashes, exclusions, restore/rollback exactness. |
| Config/profile | parse/diff/round-trip, CLI-preferred edits, protected `[Patch]`, exact-state profile switch. |
| Theme | required files, CSS validation, no remote imports by default, overwrite confirmation. |
| Audit | JS/CSS/manifest/README fixtures; block token+network, eval, obfuscation, prompt injection. |
| Repair | backup/apply after update, unsupported-build stop, restore fallback separate confirmation. |
| Platform | Windows Store, Scoop, Snap, Flatpak, APT/AUR, Homebrew, Nix/declarative diagnostics. |
| Verification | config/file/CLI/audit/doctor checks, last-known-good update only after pass. |
| Reports | JSON schema, Markdown rendering, redaction. |
| UX | novice and power-user prompts produce expected dry-run and confirmation text. |
| Invariants | non-waivable invariant tests, waiver rejection, single-writer lock, fake-CI guard. |
| Recovery | failure catalog fixtures, safe stop reports, rollback failure handling, manual-only platform actions. |

## No-live-Spotify CI guard

CI must fail if:

- real `spicetify` path is used instead of fake binary,
- real Spotify config/userdata paths are detected,
- tests write outside temp fixture roots,
- tests require network/package install by default.

## Definition of Done

- OpenSpec strict validation passes in the target environment or unavailability is documented.
- All JSON schemas parse and examples validate.
- Unit and fake integration tests pass.
- Regression prompts cover safety, platform, provenance, repair, rollback, and UX.
- No critical/high audit findings remain in the planning pack.


## Added validation focus

| Area | Required checks |
|---|---|
| Desired-state manifest | Export-current dry-run replay, unsafe override rejection, third-party missing asset handling. |
| Privacy/redaction | Token/path/log redaction, screenshot/log consent, strict-shareable report scan. |
| Scaffold templates | Generated output audit, package-script approval, Creator compatibility warning. |
| Automation | Headless dry-run authority parity, batch stop-on-failure, CI real-path guard. |

## Docs-site validation

Checks for the accompanying docs site after implementation approval:

```bash
pnpm --filter docs lint
pnpm --filter docs typecheck
pnpm --filter docs test
pnpm --filter docs build
pnpm --filter docs validate:content
```

In this repo on 2026-06-13, `pnpm install --frozen-lockfile`, `pnpm --filter docs lint`, `pnpm --filter docs typecheck`, `pnpm --filter docs build`, and `pnpm --filter docs validate:content` passed after explicit dependency/build-script approval.

Validation expectations:

- package-manager command uses the detected target-repo package manager;
- generated docs include source paths and no unresolved placeholders;
- no secrets, private user paths, prefs contents, or unredacted logs appear in docs output;
- Fumadocs content routes and search route render locally;
- `llms.txt` and full AI-readable docs routes use redacted stable docs content;
- accessibility checks cover keyboard navigation, focus, headings, dialogs, and search.

## Companion docs-site validation

When the Fumadocs + shadcn/ui site is implemented, validation MUST include equivalent target-repo checks for:

- Fumadocs MDX compilation;
- typechecking;
- linting;
- docs build;
- link integrity;
- accessibility checks for risk and confirmation components;
- redaction scan for examples, screenshots, report previews, generated references, and AI-readable routes;
- source traceability for generated schema and mode reference pages.

Proposed commands when the target repo uses pnpm workspaces:

```bash
pnpm --filter docs lint
pnpm --filter docs typecheck
pnpm --filter docs build
pnpm --filter docs test
```

Substitute equivalent commands for the actual repo.

## Subagent swarm validation

Required checks for the Codex swarm plan:

- `subagent-task-graph.md` exists and lists orchestrator, A0 through A8, dependencies, write scopes, outputs, stop conditions, merge protocol, and sequential fallback.
- `codex-kickoff-prompt.md` names read-first files, subagent sequence, allowed write scopes, validation commands, and stop conditions.
- `schemas/subagent-task-graph.schema.json` and `schemas/subagent-result.schema.json` parse as JSON.
- `openspec/changes/add-spicetify-skill/specs/agents/spec.md` uses behavior-level requirements and scenarios.
- `tasks.md` includes implementation tasks for subagent graph, kickoff prompt, and validator/eval coverage.
- Regression prompts include swarm kickoff, write-scope overlap refusal, and subagent result-envelope validation.
