# Evals and Evolve

Use this reference when a user asks `/spicetify` to evaluate, improve, harden, or evolve the skill itself.

Installed-skill payloads include this runbook, not the full repo harness. Running the deterministic eval suite requires a checkout with `tools/run_skill_evals.py`, `evals/spicetify-eval-suite.json`, `schemas/`, and fake fixtures. Installed-skill-only use may review approved redacted eval results and reports, but must not invent local runner output.

## Evolve mode

`evolve` is a meta-improvement mode. It reviews redacted eval results, operation reports, review reports, and user-provided redacted transcripts to find gaps in the skill, helper runtime, docs, or tests.

`evolve` produces an improvement plan, not an automatic patch. The plan should name:

- failing or missing evals;
- observed behavior and evidence;
- root cause category;
- proposed eval additions;
- proposed files to change;
- expected safety and quality effect;
- validation commands;
- rollback or abandon path.

## Hard boundaries

- Do not scrape private chat history or local logs automatically.
- Do not inspect real Spotify prefs contents.
- Do not upload traces, reports, or evidence to hosted eval tools.
- Do not run model-judge or hosted evals unless the user explicitly approves the provider, data scope, and credentials.
- Treat Promptfoo, model judges, and hosted eval exports as optional and non-blocking until explicitly promoted by the user.
- Do not weaken dry-run, snapshot, confirmation, audit, provenance, privacy, or no-shell rules to improve eval scores.
- Do not self-approve, commit, publish, install packages, or run package-manager commands.

## Improvement loop

1. Collect only approved, redacted inputs.
2. Score local evals and identify repeated failures.
3. Cluster failures by root cause: routing, policy, command, state, audit, privacy, docs, or invalid eval.
4. Add or update a failing eval before proposing behavior changes.
5. Propose the smallest safe skill, runtime, or docs change.
6. Compare baseline and candidate results.
7. Accept the change only when deterministic safety gates stay green and the targeted eval improves.

## Default answer shape

When `evolve` is requested and no approved eval result exists, propose a dry-run evaluation plan first. Explain which local artifacts would be read, which would be ignored, and which validation commands would run. Keep all evidence redacted and local.

Default local validation command for a repo checkout:

```bash
python3 tools/run_skill_evals.py --suite evals/spicetify-eval-suite.json --strict
python3 tools/run_skill_evals.py --suite evals/spicetify-eval-suite.json --strict --execute-fake
```
