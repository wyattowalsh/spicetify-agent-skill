# Runtime

The portable skill is installed with `npx skills`. The runtime helper is installed separately as `spicetify-agent`. The official Spicetify CLI is also installed separately by the user.

## Skill Install

Local checkout:

```bash
npx skills add <repo-checkout> --skill spicetify -y -g -a antigravity claude-code codex crush cursor gemini-cli github-copilot opencode
```

Public source after release:

```bash
npx skills add github:wyattowalsh/spicetify-agent-skill --skill spicetify -y -g -a antigravity claude-code codex crush cursor gemini-cli github-copilot opencode
```

## Helper CLI

Use `spicetify-agent` for plans, schema checks, reports, and guarded execution:

```bash
uvx --from github:wyattowalsh/spicetify-agent-skill spicetify-agent --help
uvx --from github:wyattowalsh/spicetify-agent-skill spicetify-agent plan --mode repair "spotify updated and spicetify broke"
```

From a local checkout:

```bash
uv run spicetify-agent --help
uvx --from . spicetify-agent --help
```

Do not auto-install the helper CLI, Python, Node, package-manager dependencies, or the official Spicetify CLI without explicit user approval.

## First Checks

1. Check whether `spicetify-agent --help` is available.
2. Check whether the official `spicetify` CLI is available only when local probing is needed.
3. If either is missing, report the missing dependency and offer manual install guidance.
4. In CI, never touch real Spotify or Spicetify paths.
5. In local execution, require explicit real-run opt-in and plan-hash confirmation.

## Important Names

- Skill name: `/spicetify`
- Helper command: `spicetify-agent`
- External upstream command: `spicetify`
