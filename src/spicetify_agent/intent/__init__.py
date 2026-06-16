"""Prompt-first intent routing for /spicetify."""

from .router import RouteResult, infer_route


def route_prompt(prompt: str, *, target: str | None = None) -> dict[str, object]:
    """Return a schema-shaped route dictionary for existing planner code."""

    return infer_route(prompt, target=target).to_dict()


__all__ = ["RouteResult", "infer_route", "route_prompt"]
