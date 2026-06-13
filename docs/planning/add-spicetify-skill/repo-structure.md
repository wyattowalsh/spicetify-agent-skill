# Proposed repo structure

**Path:** `docs/planning/add-spicetify-skill/repo-structure.md`
**Purpose:** Implementation repository layout for /spicetify.
**Status:** Draft
**Load/use when:** Use when creating the actual implementation repo.


```text
spicetify-skill/
  README.md
  AGENTS.md
  package.json
  pnpm-lock.yaml
  tsconfig.json
  vitest.config.ts
  openspec/
    config.yaml
    changes/add-spicetify-skill/
  skills/
    spicetify/
      SKILL.md
      references/
      schemas/
      templates/
      evals/
  src/
    cli.ts
    intent/
    core/
    spicetify/
    fs/
    state/
    modes/
    audit/
    scaffold/
    verify/
    reports/
  tests/
    unit/
    integration/
    fixtures/
      fake-spicetify-bin/
      fake-home/
      broken-states/
    golden/
  scripts/
    fake-spicetify.ts
    validate-schemas.ts
```

## Notes

- Preserve package manager detected in the target repo; use `pnpm` only for a new repo.
- Do not add hooks/MCP/plugins until they remove a repeated manual loop and are approved.
- Keep `skills/spicetify/SKILL.md` concise; references hold the depth.

## Accompanying docs app structure

Recommended docs workspace:

```text
apps/docs/
  app/
  content/docs/
  components/ui/
  components/spicetify/
  lib/
  scripts/
  source.config.ts
  next.config.mjs
  components.json
```

The docs app is intentionally separate from runtime modules. It may read OpenSpec/planning/schema files to generate reference docs, but it must not import runtime code that executes Spicetify or mutates local state.

## Companion docs site structure

Recommended when implementation is approved in a new or monorepo target:

```text
apps/docs/
  app/
  content/docs/
  components/ui/
  components/spicetify/
  lib/source.ts
  scripts/sync-openspec-content.ts
  source.config.ts
  next.config.mjs
  components.json
```

If the target repo is not a monorepo, use equivalent root-level paths. Preserve existing package manager and docs conventions unless migration is approved.
