"""Path guards for local and staged Spicetify asset intake."""

from __future__ import annotations

import re
from collections.abc import Iterable, Sequence
from pathlib import Path

from ..errors import PolicyBlocked, UnsafePath
from ..safe_paths import ensure_within, reject_symlink

REAL_SPOTIFY_PATH_PATTERNS = (
    re.compile(r"/Users/[^/]+/Library/Application Support/(Spotify|spicetify)(/|$)", re.I),
    re.compile(r"/Users/[^/]+/\.config/spicetify(/|$)", re.I),
    re.compile(r"/home/[^/]+/\.config/spicetify(/|$)", re.I),
    re.compile(r"C:\\Users\\[^\\]+\\AppData\\Roaming\\(Spotify|spicetify)(\\|$)", re.I),
    re.compile(r"/Applications/Spotify\.app(/|$)", re.I),
)


def approved_asset_roots(roots: Sequence[str | Path] | None = None) -> tuple[Path, ...]:
    """Return resolved roots under which explicit asset reads are allowed."""

    values: Iterable[str | Path] = roots if roots else (Path.cwd(),)
    resolved: list[Path] = []
    for root in values:
        root_path = Path(root).expanduser()
        if _looks_like_real_spotify_path(str(root_path)):
            raise PolicyBlocked("Real Spotify/Spicetify state paths must be staged first")
        reject_symlink(root_path)
        resolved_root = root_path.resolve()
        if not resolved_root.exists() or not resolved_root.is_dir():
            raise PolicyBlocked("Approved asset root must be an existing directory")
        reject_symlink_components(resolved_root, resolved_root)
        resolved.append(resolved_root)
    return tuple(resolved)


def resolve_asset_target(
    target: str | Path,
    *,
    roots: Sequence[str | Path] | None = None,
    must_exist: bool = True,
) -> Path:
    """Resolve an asset target only if it stays within an approved root."""

    raw = Path(target).expanduser()
    raw_text = str(target)
    if _looks_like_real_spotify_path(raw_text):
        raise PolicyBlocked("Real Spotify/Spicetify state paths must be staged first")
    if not raw.is_absolute() and ".." in raw.parts:
        raise UnsafePath(f"Path escapes root: {target}")

    allowed_roots = approved_asset_roots(roots)
    failures: list[Exception] = []
    for root in allowed_roots:
        candidate = raw if raw.is_absolute() else root / raw
        try:
            if _looks_like_real_spotify_path(str(candidate)):
                raise PolicyBlocked("Real Spotify/Spicetify state paths must be staged first")
            reject_symlink_components(root, candidate)
            resolved = ensure_within(root, candidate)
            if must_exist and not resolved.exists():
                raise PolicyBlocked("Asset target must exist under an approved asset root")
            reject_symlink_components(root, resolved)
            return resolved
        except (OSError, PolicyBlocked, UnsafePath) as exc:
            failures.append(exc)

    if failures:
        raise failures[-1]
    raise UnsafePath(f"Path escapes root: {target}")


def reject_symlink_components(root: Path, candidate: Path) -> None:
    """Reject symlinks in the root, target, or any existing path component."""

    reject_symlink(root)
    try:
        relative = candidate.relative_to(root)
    except ValueError:
        return
    current = root
    for part in relative.parts:
        current = current / part
        reject_symlink(current)


def _looks_like_real_spotify_path(value: str) -> bool:
    return any(pattern.search(value) for pattern in REAL_SPOTIFY_PATH_PATTERNS)
