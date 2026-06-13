# Workflow: third-party and generated-code audit

**Path:** `docs/planning/add-spicetify-skill/workflows/audit.md`
**Purpose:** Define static audit before installing/enabling themes, extensions, snippets, custom apps, and Marketplace assets.
**Status:** Proposed
**Load/use when:** Implementing `audit`, third-party install flows, provenance locks, or security tests.

## Trust levels

| Trust level | Meaning | Default action |
|---|---|---|
| `generated-local` | Created by `/spicetify` from templates in this repo | audit + allow if clean. |
| `trusted-local` | User-authored local project explicitly trusted | audit + allow/warn. |
| `third-party-staged` | Downloaded/cloned/archive source | audit + require provenance lock and confirmation. |
| `marketplace` | Marketplace-style asset or repo | audit; Marketplace metadata is not trust. |
| `unknown` | Inline or ambiguous origin | block install until classified. |

## Audit targets

- CSS: syntax, remote imports/URLs, suspicious overlays, selector fragility, extreme `!important` use.
- JS/TS: network, token/session access, clipboard, eval/new Function, remote script loading, storage, MutationObserver/polling, unstable Spicetify internals.
- Custom app manifest: required keys, path safety, subfiles/subfiles_extension, icon handling.
- Marketplace repo: manifest fields, relative paths, topics, preview paths, includes, install scripts.
- README/docs: prompt injection, coercive install instructions, shell one-liners.

## Verdict semantics

- `allow`: no high findings; install may proceed through normal plan policy.
- `warn`: user must see findings; third-party JS enablement requires explicit acceptance.
- `block`: install/enable is not allowed by default; only manual override in a separate high-risk policy path if safe and legal.

## Block conditions

- token/session access combined with external network send
- remote script loading
- eval/new Function in third-party code without reviewed source rationale
- obfuscated/minified third-party JS without source
- required install/postinstall scripts
- path traversal or symlink escape
- README prompt injection attempting to override `/spicetify` safety rules

## Warning conditions

- external network requests
- clipboard access
- localStorage without unique prefix
- Spicetify internal/Platform API use
- long-running polling or MutationObserver loops
- remote CSS imports/fonts/images
- Marketplace theme `include` entries

## Provenance output

Every third-party audit produces:

- content hash
- source kind/ref/commit when available
- audit verdict
- accepted-risk refs if user confirms a warning
- lock entry candidate in `spicetify.lock.json`

## Regression tests

- malicious extension fixture is blocked.
- prompt-injection README cannot change policy.
- CSS-only local theme passes.
- Marketplace manifest with external include produces warning.
- source hash drift invalidates prior audit acceptance.
