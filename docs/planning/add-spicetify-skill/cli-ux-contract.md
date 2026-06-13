# CLI and conversational UX contract

**Path:** `docs/planning/add-spicetify-skill/cli-ux-contract.md`
**Purpose:** Define the human-facing and JSON-facing interaction contract for novices, power users, dry-runs, confirmations, and reports.
**Status:** Proposed
**Load/use when:** Implementing CLI output, assistant responses, operation summaries, confirmations, or regression prompts.

## Interaction principles

- Prefer semantic modes over raw commands.
- Show the smallest useful summary first; link or attach structured detail for power users.
- Every mutating response starts with a dry-run plan summary, then the structured plan.
- Dangerous requests refuse the unsafe part and offer a safe diagnostic, audit, or manual checklist.
- JSON is canonical for tools; prose is derived from validated structured objects.

## Progressive disclosure by user type

| User posture | Default output | Expand on request |
|---|---|---|
| Novice | concise diagnosis, risk, proposed next safe action | why each command/file matters, rollback explanation |
| Power user | plan summary plus JSON path/report IDs | full command/mutation diff, provenance, verification evidence |
| Automation | JSON only by default, no authority expansion | Markdown report artifact after redaction |
| Developer | build/watch/audit loops with bounded logs | DevTools consent scope and source maps if safe |

## Confirmation copy requirements

A confirmation prompt MUST name:

- mode and plan ID;
- exact risk class;
- snapshot ID or required snapshot action;
- commands to run as argv arrays;
- files to create/overwrite/delete;
- third-party sources and audit verdicts;
- rollback path;
- stop conditions;
- expiry or drift invalidation rule.

It MUST NOT ask for blanket permission such as “do whatever is needed.”

## Output examples

### Dry-run summary

```text
/spicetify planned a safe theme switch. Nothing has been changed yet.
Risk: medium. Snapshot required. Confirmation required before apply.
Will change: current_theme, color_scheme, one theme folder.
Will run: ["spicetify", "config", ...], then ["spicetify", "apply"].
Rollback: restore snapshot <id> and re-apply prior config.
```

### Blocked action

```text
I will not run installer scripts or arbitrary shell. I can stage the source, audit it, and produce a manual checklist instead.
```

### Recovery failure summary

```text
Repair stopped before the fallback reset because the primary apply failed and the fallback requires separate confirmation.
Snapshot is available. Last-known-good was not changed.
```

## Accessibility and ergonomics

- Use stable terms: `dry-run`, `snapshot`, `plan`, `verify`, `rollback`, `manual-only`, `blocked`.
- Keep error codes short and searchable.
- Avoid hiding high-risk actions behind friendly phrasing.
- Provide one recommended next safe action, not a long menu, unless the user asks for options.
