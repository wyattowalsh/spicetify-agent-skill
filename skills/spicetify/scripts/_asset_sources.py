"""Read-only source discovery helpers for Spicetify ecosystem assets."""

from __future__ import annotations

from typing import Any

TOPICS = {
    "extension": "spicetify-extensions",
    "theme": "spicetify-themes",
    "custom-app": "spicetify-apps",
    "snippet": "spicetify",
    "marketplace": "spicetify",
    "unknown": "spicetify",
}


def discover_sources(
    query: str, *, asset_kind: str, source: str | None = None, allow_network: bool = False
) -> list[dict[str, Any]]:
    """Return metadata-only source candidates without fetching or executing code."""

    if source:
        return [_source_from_user_input(source, asset_kind=asset_kind)]
    topic = TOPICS.get(asset_kind, "spicetify")
    source_kind = "github-topic" if asset_kind != "marketplace" else "marketplace-metadata"
    return [
        {
            "sourceId": f"{source_kind}:{topic}",
            "kind": source_kind,
            "assetKind": asset_kind,
            "query": query,
            "locator": f"https://github.com/topics/{topic}",
            "pinnedRef": None,
            "confidence": "low",
            "networkRequired": True,
            "networkApproved": allow_network,
            "metadataOnly": True,
            "trusted": False,
            "notes": [
                "Discovery metadata only",
                "Network approval does not fetch or trust code in this implementation",
                "Requires immutable ref and staged audit before any install plan",
            ],
        }
    ]


def _source_from_user_input(source: str, *, asset_kind: str) -> dict[str, Any]:
    source_kind = "github-repo" if "github.com" in source.lower() else "user-source"
    return {
        "sourceId": f"{source_kind}:{source}",
        "kind": source_kind,
        "assetKind": asset_kind,
        "query": source,
        "locator": source,
        "pinnedRef": None,
        "confidence": "medium",
        "networkRequired": source_kind == "github-repo",
        "networkApproved": False,
        "metadataOnly": True,
        "trusted": False,
        "notes": ["User-provided source; still untrusted until staged and audited"],
    }
