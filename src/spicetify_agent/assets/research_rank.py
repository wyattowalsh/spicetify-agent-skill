"""Explainable ranking for read-only ecosystem research candidates."""

from __future__ import annotations

from typing import Any


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
