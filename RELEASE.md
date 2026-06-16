# Release Checklist

## v0.1.0

Release only from a clean `main` tree after the validation commands in this
checklist pass.

### Version Surfaces

- `pyproject.toml` declares `0.1.0`.
- `skills/spicetify/scripts/spicetify_agent.py` reports `spicetify-agent 0.1.0`.
- `agent-bundle.json`, plugin metadata, and `skills/spicetify/agents/openai.yaml`
  declare `0.1.0`.
- README, skill runtime reference, changelog, and docs release checklist point to
  `v0.1.0`.

### Blocking Validation

```bash
git status --short --branch --untracked-files=all
uv lock --offline
PYTHONDONTWRITEBYTECODE=1 uv run --frozen pytest
uv run --frozen ruff format --check .
uv run --frozen ruff check .
PYTHONPATH=skills/spicetify/scripts PYTHONDONTWRITEBYTECODE=1 uv run --frozen ty check skills/spicetify/scripts tools tests
python3 tools/validate_bundle.py --root . --write-manifest
python3 tools/validate_bundle.py --root .
python3 tools/validate_openspec_structure.py --root .
python3 -m json.tool evals/regression-prompts.json >/dev/null
python3 tools/run_skill_evals.py --suite evals/spicetify-eval-suite.json --strict --execute-fake --json
python3 tools/run_skill_evals.py --suite evals/spicetify-routing-eval-suite.json --strict --json
python3 tools/run_skill_evals.py --suite evals/spicetify-research-eval-suite.json --strict --json
uv build
uvx --from . spicetify-agent --help
npx skills add . --skill spicetify --list
HOME="$(mktemp -d)" XDG_CONFIG_HOME="$(mktemp -d)" npx skills add . --skill spicetify -y -g -a codex
npx --yes --package @fission-ai/openspec@1.4.1 openspec validate add-spicetify-skill --strict
npx --yes --package @fission-ai/openspec@1.4.1 openspec validate --all --strict
pnpm --filter docs lint
pnpm --filter docs typecheck
pnpm --filter docs validate:content
pnpm --filter docs build
```

### Release Actions

1. Commit the release-prep changes.
2. Tag the release as `v0.1.0`.
3. Push `main` and the tag.
4. Create the GitHub release with `CHANGELOG.md` notes for `v0.1.0`.
5. Verify the public skill install command:

```bash
npx skills add github:wyattowalsh/spicetify-agent-skill@v0.1.0 --skill spicetify --list
```

Do not publish packages, deploy docs, bundle Spicetify, or run real Spicetify as
part of this release checklist.
