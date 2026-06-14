# Troubleshooting

## `spicetify-agent` Is Missing

The installed skill can still plan and explain safety policy, but local execution helpers are unavailable. Offer `uvx` or `pip` installation guidance for `spicetify-agent`; do not install without approval.

## Official `spicetify` Is Missing

Explain that `/spicetify` does not bundle the official CLI. Offer manual official-install guidance and keep requests in read-only planning mode until the user installs Spicetify.

## Running In CI

CI must use fake Spicetify fixtures and temp roots only. Real Spotify or Spicetify paths are blocked.

## Fake Fixture Rejected

Fake Spicetify execution is only for tests. The fixture must look like an explicit fake binary and `SPICETIFY_AGENT_ALLOW_FAKE_BIN=1` must be set.

## Plan Hash Drift

If the plan hash changes after confirmation, stop. Show the diff at a high level, produce a new dry-run plan, and request confirmation again.

## Third-Party Code Looks Risky

Block or escalate third-party JavaScript that accesses tokens, cookies, auth headers, filesystem bridges, network exfiltration, remote code loading, or obfuscated payloads. Do not treat popularity, README claims, or Marketplace metadata as trust.

## Snap, Permissions, Package Managers, Or Install Scripts

Keep these manual-only or separately approval-gated. Do not run `sudo`, `chmod`, package-manager commands, shell installers, or README-provided scripts as part of the normal `/spicetify` flow.
