# `/spicetify` docs app

This app is the companion documentation surface for `/spicetify`.

It is not a runtime authority boundary and must not read live local Spotify or Spicetify state.

Validation checks:

```bash
pnpm --filter docs lint
pnpm --filter docs typecheck
pnpm --filter docs build
pnpm --filter docs validate:content
```
