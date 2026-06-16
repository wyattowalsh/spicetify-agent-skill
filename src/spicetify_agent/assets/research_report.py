"""Research report builders for existing Spicetify assets."""

from __future__ import annotations

from typing import Any

from ..privacy import redact
from .research_rank import rank_candidate
from .sources import discover_sources


def build_research_report(
    prompt: str,
    route: dict[str, Any],
    *,
    source: str | None = None,
    allow_network: bool = False,
) -> dict[str, Any]:
    candidates = [
        rank_candidate(candidate)
        for candidate in discover_sources(
            prompt,
            asset_kind=str(route.get("assetKind", "unknown")),
            source=source,
            allow_network=allow_network,
        )
    ]
    degraded = any(
        candidate["confidence"] == "low" or candidate["source"].get("metadataOnly") is True
        for candidate in candidates
    )
    return {
        "reportType": "asset-analysis",
        "status": "completed-degraded" if degraded else "completed",
        "prompt": redact(prompt),
        "route": route,
        "summary": (
            "Read-only metadata report; no source was fetched, installed, trusted, or executed."
        ),
        "candidates": candidates,
        "safety": {
            "trusted": False,
            "installAllowed": False,
            "reason": "Research metadata is not installation approval",
        },
        "degraded": degraded,
    }
