# Prompt Router

Use natural language as the public interface:

```text
/spicetify <prompt input>
```

Do not require the user to choose a mode. Infer the route, then choose the safest next artifact.

| User intent | Internal route | Next artifact |
|---|---|
| Find or compare existing assets | `research` | research report |
| Ask if an extension/theme/app/snippet is safe | `inspect -> audit` | audit report |
| Install or enable a GitHub/Marketplace asset safely | `pin -> stage -> inspect -> audit -> plan` | dry-run plan |
| Create a local theme, extension, or custom app | `create -> audit -> plan` | dry-run plan |
| Repair broken Spicetify after an update | `repair` | dry-run plan |
| Watch or debug local development | `debug/watch` | consent-gated plan |
| Improve the skill from eval results | `evolve` | improvement plan |
| Run shell, package-manager, or installer commands | `refuse/manual-only` | refusal or manual guidance |

Internal mode combinations are allowed, but mutation still requires one plan hash, one snapshot policy, and one explicit confirmation flow.
