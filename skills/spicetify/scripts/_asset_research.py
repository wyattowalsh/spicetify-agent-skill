"""Research ranking and reports for existing Spicetify assets."""

from __future__ import annotations

from typing import Any

from _asset_sources import discover_sources
from _privacy import redact


def rank_candidate(source: dict[str, Any]) -> dict[str, Any]:
    asset_kind = str(source.get("assetKind", "unknown"))
    risk_findings = ["third-party source requires audit"]
    if source.get("pinnedRef") is None:
        risk_findings.append("source is not pinned to an immutable ref")
    if source.get("kind") in {"github-topic", "marketplace-metadata"}:
        risk_findings.append("metadata presence is not a trust signal")
    return {
        "assetKind": asset_kind,
        "source": source,
        "manifestStatus": "unknown-until-staged",
        "compatibilitySignals": _compatibility_signals(asset_kind),
        "maintenanceSignals": ["not evaluated without source staging"],
        "riskFindings": risk_findings,
        "provenanceReadiness": "requires-pinned-source",
        "confidence": source.get("confidence", "low"),
        "recommendedNextAction": "pin-and-stage-for-audit",
    }


def _compatibility_signals(asset_kind: str) -> list[str]:
    if asset_kind == "extension":
        return ["expect JS or MJS extension asset", "verify Spicetify API wait pattern"]
    if asset_kind == "theme":
        return ["expect color.ini and user.css", "audit optional theme.js"]
    if asset_kind == "custom-app":
        return ["distinguish raw manifest.json from Creator src/settings.json"]
    if asset_kind == "snippet":
        return ["distinguish CSS-only snippet from executable JS"]
    if asset_kind == "marketplace":
        return ["validate Marketplace metadata without assigning trust"]
    return ["asset kind unknown until source inspection"]


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
