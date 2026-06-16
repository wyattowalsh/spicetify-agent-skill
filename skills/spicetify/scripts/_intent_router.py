"""Natural-language route inference for prompt-first /spicetify usage."""

from __future__ import annotations

import re
from dataclasses import dataclass

from _policy import classify_prompt

ASSET_KEYWORDS = {
    "custom-app": ("custom app", "custom-app", "customapp"),
    "extension": ("extension", "extensions", ".js", ".mjs"),
    "theme": ("theme", "themes", "color.ini", "user.css"),
    "snippet": ("snippet", "snippets"),
    "marketplace": ("marketplace",),
}
RESEARCH_KEYWORDS = (
    "find",
    "search",
    "research",
    "recommend",
    "compare",
    "popular",
    "existing",
    "available",
)
CREATE_KEYWORDS = (
    "create",
    "make a",
    "make an",
    "make me",
    "generate",
    "scaffold",
    "build me",
    "new",
)
AUDIT_KEYWORDS = ("audit", "safe", "review", "is this", "check")
INSTALL_KEYWORDS = (
    "install this",
    "install",
    "enable this",
    "enable",
    "apply the plan",
    "apply this",
    "apply",
    "switch to",
    "add this",
    "use this",
)
DEBUG_KEYWORDS = ("debug", "devtools", "logs", "watch", "hot reload", "hot-reload")
REPAIR_KEYWORDS = ("repair", "fix", "broke", "broken", "restore", "rollback")
EVOLVE_KEYWORDS = ("evolve", "eval", "improve the skill", "optimize the skill")
GITHUB_MARKERS = (
    "github.com",
    "github:",
    "github ",
    "spicetify-extensions",
    "spicetify-themes",
)
LOCAL_MARKERS = ("file:", "./", "../", ".css", ".ini", ".js", ".mjs", ".json")
SUBSTRING_CUES = {
    "./",
    "../",
    ".css",
    ".ini",
    ".js",
    ".mjs",
    ".json",
    "file:",
    "github.com",
    "github:",
    "color.ini",
    "user.css",
}


@dataclass(frozen=True)
class RouteResult:
    prompt: str
    primary_intent: str
    secondary_intents: tuple[str, ...]
    asset_kind: str
    source_kind: str
    risk: str
    confidence: float
    next_artifact: str
    requires_network_approval: bool
    requires_snapshot: bool
    requires_confirmation: bool
    blocked_reason: str | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "prompt": self.prompt,
            "primaryIntent": self.primary_intent,
            "secondaryIntents": list(self.secondary_intents),
            "assetKind": self.asset_kind,
            "sourceKind": self.source_kind,
            "risk": self.risk,
            "confidence": self.confidence,
            "nextArtifact": self.next_artifact,
            "requiresNetworkApproval": self.requires_network_approval,
            "requiresSnapshot": self.requires_snapshot,
            "requiresConfirmation": self.requires_confirmation,
            "blockedReason": self.blocked_reason,
        }


def infer_route(prompt: str, *, target: str | None = None) -> RouteResult:
    """Infer the safest next artifact from a natural-language /spicetify prompt."""

    text = f"{prompt} {target or ''}".strip()
    lowered = normalize_text(text)
    policy = classify_prompt(text)
    asset_kind = _asset_kind(lowered)
    source_kind = _source_kind(lowered, target)
    if not policy.allowed:
        return RouteResult(
            prompt=prompt,
            primary_intent="refuse",
            secondary_intents=(),
            asset_kind=asset_kind,
            source_kind=source_kind,
            risk="blocked",
            confidence=1.0,
            next_artifact="refusal",
            requires_network_approval=False,
            requires_snapshot=False,
            requires_confirmation=False,
            blocked_reason=policy.reason,
        )

    primary = _primary_intent(lowered)
    if primary == "create" and asset_kind == "unknown":
        primary = "inspect"
    secondary = _secondary_intents(lowered, primary)
    confidence = _confidence(lowered, primary, asset_kind)
    risk = _risk(primary, source_kind, lowered)
    next_artifact = _next_artifact(primary, risk, confidence)
    requires_network = primary == "research" and source_kind in {
        "github",
        "marketplace",
        "unknown",
    }
    requires_snapshot = (
        primary in {"install-plan", "create", "repair", "debug"} and risk != "blocked"
    )
    requires_confirmation = requires_snapshot or risk == "high"
    return RouteResult(
        prompt=prompt,
        primary_intent=primary,
        secondary_intents=secondary,
        asset_kind=asset_kind,
        source_kind=source_kind,
        risk=risk,
        confidence=confidence,
        next_artifact=next_artifact,
        requires_network_approval=requires_network,
        requires_snapshot=requires_snapshot,
        requires_confirmation=requires_confirmation,
    )


def _asset_kind(text: str) -> str:
    for kind, markers in ASSET_KEYWORDS.items():
        if has_any_cue(text, markers):
            return kind
    return "unknown"


def _source_kind(text: str, target: str | None) -> str:
    if has_any_cue(text, GITHUB_MARKERS):
        return "github"
    if contains_cue(text, "marketplace"):
        return "marketplace"
    if target or has_any_cue(text, LOCAL_MARKERS):
        return "local"
    if has_any_cue(text, CREATE_KEYWORDS):
        return "generated"
    return "unknown"


def _primary_intent(text: str) -> str:
    if has_any_cue(text, EVOLVE_KEYWORDS):
        return "evolve"
    if has_any_cue(text, REPAIR_KEYWORDS):
        return "repair"
    if has_any_cue(text, DEBUG_KEYWORDS):
        return "debug"
    if has_any_cue(text, CREATE_KEYWORDS):
        return "create"
    if has_any_cue(text, RESEARCH_KEYWORDS):
        return "research"
    if has_any_cue(text, INSTALL_KEYWORDS):
        return "install-plan"
    if has_any_cue(text, AUDIT_KEYWORDS):
        return "audit"
    return "inspect"


def _secondary_intents(text: str, primary: str) -> tuple[str, ...]:
    found: list[str] = []
    for intent, markers in (
        ("research", RESEARCH_KEYWORDS),
        ("audit", AUDIT_KEYWORDS),
        ("install-plan", INSTALL_KEYWORDS),
        ("debug", DEBUG_KEYWORDS),
    ):
        if intent != primary and has_any_cue(text, markers):
            found.append(intent)
    return tuple(found)


def _confidence(text: str, primary: str, asset_kind: str) -> float:
    score = 0.35
    if contains_cue(text, "/spicetify") or contains_cue(text, "spicetify"):
        score += 0.2
    if primary != "inspect":
        score += 0.2
    if asset_kind != "unknown":
        score += 0.2
    if has_any_cue(text, GITHUB_MARKERS):
        score += 0.05
    return min(score, 0.95)


def _risk(primary: str, source_kind: str, text: str) -> str:
    if primary == "refuse":
        return "blocked"
    if primary in {"research", "inspect"}:
        return "low"
    if primary in {"audit", "evolve"}:
        return "medium"
    if primary in {"debug", "repair"}:
        return "high"
    if source_kind in {"github", "marketplace"}:
        return "high"
    if contains_cue(text, "third-party") or contains_cue(text, "download"):
        return "high"
    return "medium"


def _next_artifact(primary: str, risk: str, confidence: float) -> str:
    if risk == "blocked" or primary == "refuse":
        return "refusal"
    if confidence < 0.45:
        return "clarification"
    if primary == "research":
        return "research-report"
    if primary == "audit":
        return "audit-report"
    if primary in {"create", "install-plan", "repair", "debug"}:
        return "dry-run-plan"
    if primary == "evolve":
        return "dry-run-plan"
    return "answer"


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.casefold()).strip()


def has_any_cue(text: str, cues: tuple[str, ...]) -> bool:
    return any(contains_cue(text, cue) for cue in cues)


def contains_cue(text: str, cue: str) -> bool:
    normalized_text = normalize_text(text)
    normalized_cue = normalize_text(cue)
    if not normalized_cue:
        return False
    if normalized_cue in SUBSTRING_CUES or normalized_cue.startswith("/"):
        return normalized_cue in normalized_text
    parts = [re.escape(part) for part in normalized_cue.split()]
    pattern = r"(?<![\w-])" + r"\s+".join(parts) + r"(?![\w-])"
    return re.search(pattern, normalized_text) is not None


def route_prompt(prompt: str, *, target: str | None = None) -> dict[str, object]:
    """Return a schema-shaped route dictionary for planner code."""

    return infer_route(prompt, target=target).to_dict()
