# Changelog

## v0.1.0 - 2026-06-16

Initial release of the portable `/spicetify` Agent Skill and `spicetify-agent`
helper CLI.

- Ships a self-contained skill payload under `skills/spicetify/` with compact
  trigger guidance, references, inert assets, metadata-only agent hints, and
  flat Python helper scripts.
- Provides `spicetify-agent` as the installable helper command without creating
  a command named `spicetify`.
- Keeps the official Spicetify CLI external and never bundles or auto-installs
  it.
- Preserves dry-run-first planning, allowlisted argv execution, fake-only CI,
  path guards, snapshots, plan-hash confirmations, verification, redaction,
  reports, and rollback paths.
- Adds prompt-first `/spicetify <prompt>` routing, metadata-only asset research,
  audit and provenance workflows, eval suites, and the `evolve` improvement
  loop.
- Moves durable documentation to the Fumadocs app under `apps/docs/` and removes
  the root `docs/` tree.
