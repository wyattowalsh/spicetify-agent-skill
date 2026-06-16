"""Command line interface for the installable spicetify-agent tool."""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import cast

__version__ = "0.1.0"

from _commands import validate_command_invocation
from _errors import PolicyBlocked, SpicetifyAgentError
from _modes import ALL_MODES, MUTATING_MODES, plan_mode
from _policy import PolicyDecision, evaluate_plan, require_confirmation
from _reports import json_report, markdown_report
from _runner import FAKE_BINARY_ENV, SpicetifyRunner
from _schemas import parse_all_schemas
from _state import snapshot_tree
from _util import stable_hash
from _verify import verify_command_results


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="spicetify-agent",
        description="Dry-run-first /spicetify operator around the Spicetify CLI.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--json", action="store_true", help="Emit JSON output.")
    parser.add_argument("--markdown", action="store_true", help="Emit Markdown report output.")
    sub = parser.add_subparsers(dest="command")

    plan = sub.add_parser("plan", help="Build a dry-run plan from a prompt.")
    plan.add_argument("prompt", nargs="*", help="Prompt text after /spicetify.")
    plan.add_argument("--mode", choices=ALL_MODES, default="plan")
    plan.add_argument("--target")
    plan.add_argument(
        "--asset-root",
        type=Path,
        action="append",
        help="Approved local/staged asset root for --target audit or inspect reads.",
    )
    plan.add_argument(
        "--allow-network-research",
        action="store_true",
        help="Mark ecosystem research as user-approved for network discovery.",
    )

    research = sub.add_parser("research", help="Build a read-only research report from a prompt.")
    research.add_argument("prompt", nargs="*", help="Research prompt after /spicetify.")
    research.add_argument("--target")
    research.add_argument(
        "--asset-root",
        type=Path,
        action="append",
        help="Approved local/staged asset root for --target audit or inspect reads.",
    )
    research.add_argument(
        "--allow-network-research",
        action="store_true",
        help="Mark ecosystem research as user-approved for network discovery.",
    )

    for mode in ALL_MODES:
        if mode == "plan":
            continue
        cmd = sub.add_parser(mode, help=f"Build a dry-run plan for {mode}.")
        cmd.add_argument("prompt", nargs="*", help="Optional prompt text.")
        cmd.add_argument("--target")
        cmd.add_argument(
            "--asset-root",
            type=Path,
            action="append",
            help="Approved local/staged asset root for --target audit or inspect reads.",
        )
        cmd.add_argument(
            "--allow-network-research",
            action="store_true",
            help=argparse.SUPPRESS,
        )

    apply = sub.add_parser("execute-plan", help="Execute a saved plan through the guarded runner.")
    apply.add_argument("plan_file", type=Path)
    apply.add_argument("--confirm", help="Must match the plan hash for mutating plans.")
    apply.add_argument(
        "--allow-real", action="store_true", help="Allow real local Spicetify execution."
    )
    apply.add_argument(
        "--fake-bin",
        help="Path to fake Spicetify binary for tests; requires test-fixture opt-in env.",
    )
    apply.add_argument("--userdata-root", type=Path, help="Spicetify userdata root to snapshot.")
    apply.add_argument("--state-root", type=Path, help="spicetify-agent state/snapshot root.")

    sub.add_parser("validate-schemas", help="Parse bundled JSON schemas.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = _dispatch(args, parser)
    except SpicetifyAgentError as exc:
        payload = {"status": "error", "code": exc.code, "message": str(exc)}
        sys.stderr.write(json.dumps(payload, indent=2) + "\n")
        return 2
    except Exception as exc:  # pragma: no cover - CLI boundary
        payload = {"status": "error", "code": "unexpected_error", "message": str(exc)}
        sys.stderr.write(json.dumps(payload, indent=2) + "\n")
        return 1
    if result is None:
        return 0
    if args.markdown:
        sys.stdout.write(markdown_report(result))
    else:
        sys.stdout.write(json_report(result))
    return 0


def _dispatch(
    args: argparse.Namespace, parser: argparse.ArgumentParser
) -> dict[str, object] | None:
    if args.command is None:
        parser.print_help()
        return None
    if args.command == "validate-schemas":
        parsed = parse_all_schemas()
        return {"status": "ok", "schemas": parsed}
    if args.command == "execute-plan":
        return _execute_plan(args)
    if args.command == "plan":
        prompt = " ".join(args.prompt)
        return plan_mode(
            args.mode,
            prompt=prompt,
            target=args.target,
            allow_network_research=args.allow_network_research,
            asset_roots=args.asset_root,
        )
    if args.command == "research":
        prompt = " ".join(args.prompt)
        return plan_mode(
            "plan",
            prompt=f"/spicetify research {prompt}",
            target=args.target,
            allow_network_research=args.allow_network_research,
            asset_roots=args.asset_root,
        )
    prompt = " ".join(getattr(args, "prompt", []))
    return plan_mode(
        args.command,
        prompt=prompt,
        target=getattr(args, "target", None),
        allow_network_research=getattr(args, "allow_network_research", False),
        asset_roots=getattr(args, "asset_root", None),
    )


def _execute_plan(args: argparse.Namespace) -> dict[str, object]:
    plan = _load_verified_plan(args.plan_file)
    if plan.get("status") == "blocked":
        raise PolicyBlocked("Blocked plans cannot be executed")
    mutates = bool(plan.get("mutates"))
    snapshot_manifest: dict[str, object] | None = None
    decision = _decision_from_plan(plan)
    command_values = plan.get("commands", [])
    if not isinstance(command_values, list):
        raise SpicetifyAgentError("Plan commands must be an array", code="invalid_plan")
    if mutates and not command_values and plan.get("mode") != "snapshot":
        raise SpicetifyAgentError(
            "Mutating plans without executable steps cannot be executed",
            code="no_executable_commands",
        )
    if decision.requires_confirmation:
        require_confirmation(str(plan["planHash"]), args.confirm, decision)
    if mutates:
        snapshot_value = plan.get("snapshot")
        snapshot_info: dict[str, object] = (
            cast(dict[str, object], snapshot_value) if isinstance(snapshot_value, dict) else {}
        )
        if snapshot_info.get("required") is not False:
            if args.userdata_root is None or args.state_root is None:
                raise SpicetifyAgentError(
                    "Mutating plans require --userdata-root and --state-root "
                    "for snapshot protection",
                    code="snapshot_required",
                )
            if not args.userdata_root.exists() or not args.userdata_root.is_dir():
                raise SpicetifyAgentError(
                    f"userdata root does not exist or is not a directory: {args.userdata_root}",
                    code="invalid_userdata_root",
                )
            snapshot_manifest = snapshot_tree(args.userdata_root, args.state_root / "snapshots")
    runner = SpicetifyRunner(fake_binary=args.fake_bin, allow_real=args.allow_real)
    results: list[dict[str, object]] = []
    for command in command_values:
        if not isinstance(command, dict):
            continue
        result = runner.run(cast(dict[str, object], command))
        results.append(result.__dict__)
        if result.returncode != 0:
            break
    verification = verify_command_results(results)
    return {
        "status": "verified" if verification["ok"] else "failed",
        "mode": plan.get("mode"),
        "planHash": plan.get("planHash"),
        "fake": bool(args.fake_bin or os.environ.get(FAKE_BINARY_ENV)),
        "snapshot": snapshot_manifest,
        "results": results,
        "verification": verification,
        "rollback": plan.get("rollback"),
    }


def _load_verified_plan(path: Path) -> dict[str, object]:
    with path.open("r", encoding="utf-8") as fh:
        raw_plan = json.load(fh)
    if not isinstance(raw_plan, dict):
        raise SpicetifyAgentError("Plan file must contain a JSON object", code="invalid_plan")

    stored_hash = raw_plan.get("planHash")
    if not isinstance(stored_hash, str):
        raise SpicetifyAgentError("Plan file is missing planHash", code="plan_hash_missing")

    raw_commands = raw_plan.get("commands", [])
    if not isinstance(raw_commands, list):
        raise SpicetifyAgentError("Plan commands must be an array", code="invalid_plan")
    commands: list[dict[str, object]] = []
    for command in raw_commands:
        if not isinstance(command, dict):
            raise SpicetifyAgentError("Plan commands must be objects", code="invalid_plan")
        commands.append(validate_command_invocation(command))

    canonical = dict(raw_plan)
    canonical.pop("planHash", None)
    canonical["commands"] = commands
    if canonical.get("status") == "blocked":
        policy = canonical.get("policy")
        if commands or canonical.get("mutates") is not False or not isinstance(policy, dict):
            raise SpicetifyAgentError("Blocked plan contents drifted", code="plan_policy_drift")
        if policy.get("allowed") is not False:
            raise SpicetifyAgentError(
                "Blocked plan policy drift detected", code="plan_policy_drift"
            )
        actual_hash = stable_hash(canonical)
        if stored_hash != actual_hash:
            raise SpicetifyAgentError(
                "Plan hash does not match executable contents",
                code="plan_hash_mismatch",
            )
        canonical["planHash"] = actual_hash
        return canonical

    mode = str(canonical.get("mode", ""))
    status = str(canonical.get("status", ""))
    mutating_command = any(bool(command.get("mutates")) for command in commands)
    mutating_mode = mode in MUTATING_MODES and not (mode == "update" and not commands)
    canonical["mutates"] = mutating_command or (mutating_mode and status != "blocked")
    snapshot_value = canonical.get("snapshot")
    snapshot: dict[str, object] = snapshot_value if isinstance(snapshot_value, dict) else {}
    if canonical["mutates"]:
        snapshot = {**snapshot, "required": True}
    canonical["snapshot"] = snapshot
    policy = evaluate_plan(canonical).to_dict()
    if raw_plan.get("policy") != policy:
        raise SpicetifyAgentError("Plan policy drift detected", code="plan_policy_drift")
    canonical["policy"] = policy

    actual_hash = stable_hash(canonical)
    if stored_hash != actual_hash:
        raise SpicetifyAgentError(
            "Plan hash does not match executable contents",
            code="plan_hash_mismatch",
        )
    canonical["planHash"] = actual_hash
    return canonical


def _decision_from_plan(plan: dict[str, object]) -> PolicyDecision:
    policy = plan.get("policy") if isinstance(plan.get("policy"), dict) else {}
    policy_dict = cast(dict[str, object], policy)
    return PolicyDecision(
        risk=str(policy_dict.get("risk", "medium")),
        allowed=bool(policy_dict.get("allowed", True)),
        requires_confirmation=bool(policy_dict.get("requiresConfirmation", True)),
        reason=str(policy_dict.get("reason", "confirmation required")),
    )


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
