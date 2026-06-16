"""Inert asset workflow plan builders."""

from __future__ import annotations

from typing import Any


def build_asset_workflow_plan(route: dict[str, Any]) -> dict[str, Any]:
    primary = str(route.get("primaryIntent", "inspect"))
    asset_kind = str(route.get("assetKind", "unknown"))
    steps = _steps_for(primary, asset_kind, list(route.get("secondaryIntents", [])))
    return {
        "planType": "asset-workflow-plan",
        "assetKind": asset_kind,
        "stateMachine": [
            "discovered",
            "pinned",
            "staged",
            "inspected",
            "audited",
            "planned",
            "confirmed",
            "executed",
            "verified",
            "rollbackable",
        ],
        "steps": steps,
        "containsShell": False,
        "executesPackageManager": False,
        "trusted": False,
    }


def _steps_for(primary: str, asset_kind: str, secondary: list[str]) -> list[dict[str, Any]]:
    labels = [primary, *secondary]
    if primary in {"create", "install-plan", "debug"} and "dry-run-plan" not in labels:
        labels.append("dry-run-plan")
    return [
        {
            "id": label,
            "assetKind": asset_kind,
            "status": "planned",
            "manualOnly": label in {"build", "package-manager", "devtools", "watch"},
        }
        for label in labels
    ]
