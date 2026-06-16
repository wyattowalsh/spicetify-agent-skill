#!/usr/bin/env python3
"""Run local, deterministic /spicetify skill evals.

The runner is standard-library only, fake-environment first, and intentionally
does not discover or execute a real Spicetify binary. It evaluates activation,
structured plans, policy/command facts, fixture-backed state, traces, reports,
redaction, and optional fake execution through spicetify-agent's guarded runner.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_ROOT = ROOT / "skills" / "spicetify" / "scripts"
FIXTURE_ROOT = ROOT / "tests" / "fixtures" / "evals"
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from _modes import ALL_MODES, plan_mode  # noqa: E402
from _privacy import redact  # noqa: E402

SHELL_MARKERS = ("|", "&&", ";", "`", "$(", ">", "<")
PACKAGE_MANAGER_MARKERS = (
    "npm",
    "pnpm",
    "yarn",
    "pip",
    "brew",
    "apt",
    "apt-get",
    "winget",
    "choco",
)
INSTALLER_MARKERS = ("curl", "wget", "bash", " sh ", "sudo", "chmod", "chown")
REAL_PATH_REGEXES = (
    re.compile(r"/Users/[^/]+/Library/Application Support/(Spotify|spicetify)"),
    re.compile(r"/home/[^/]+/\.config/spicetify"),
    re.compile(r"C:\\Users\\[^\\]+\\AppData\\Roaming\\(Spotify|spicetify)", re.I),
    re.compile(r"/Applications/Spotify\.app"),
)
HOSTED_PROVIDER_MARKERS = ("openai", "anthropic", "braintrust", "langsmith", "promptfoo")
EXECUTABLE_TEXT_REGEXES: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "package-manager command",
        re.compile(r"(?<![\w-])(?:npm|pnpm)\s+(?:install|run|exec|dlx)(?![\w-])", re.I),
    ),
    (
        "package-manager command",
        re.compile(r"(?<![\w-])yarn\s+(?:install|add|run|exec|dlx)(?![\w-])", re.I),
    ),
    ("package-manager command", re.compile(r"(?<![\w-])npx(?![\w-])", re.I)),
    ("package-manager command", re.compile(r"(?<![\w-])pip\s+install(?![\w-])", re.I)),
    (
        "package-manager command",
        re.compile(r"(?<![\w-])(?:brew|apt|apt-get|winget|choco)\s+install(?![\w-])", re.I),
    ),
    (
        "installer shell pipeline",
        re.compile(
            r"(?<![\w-])(?:curl|wget)(?![\w-]).{0,120}\|.{0,40}(?<![\w-])(?:sh|bash)(?![\w-])",
            re.I | re.S,
        ),
    ),
    ("shell execution", re.compile(r"(?<![\w-])(?:bash|sh|powershell|iwr|iex)(?![\w-])", re.I)),
    ("privileged filesystem command", re.compile(r"(?<![\w-])(?:sudo|chmod|chown)(?![\w-])", re.I)),
)


def as_dict(value: Any) -> dict[str, Any]:
    return cast(dict[str, Any], value) if isinstance(value, dict) else {}


def as_list(value: Any) -> list[Any]:
    return cast(list[Any], value) if isinstance(value, list) else []


TRACE_MATCHES = {"exact", "contains-in-order", "unordered-subset", "forbidden"}
ACTIVATION_KINDS = {"direct-mode", "route-mode", "negative-trigger"}
SYNTHETIC_SECRET_PREFIX = "FAKE_SPICETIFY_EVAL_"  # noqa: S105 - synthetic leak canary


@dataclass
class CaseResult:
    id: str
    mode: str | None
    category: str | None
    status: str = "passed"
    failures: list[str] = field(default_factory=list)
    artifacts: dict[str, Any] = field(default_factory=dict)
    repeats: list[dict[str, Any]] = field(default_factory=list)
    grader_results: list[dict[str, str]] = field(default_factory=list)

    def fail(self, message: str) -> None:
        self.status = "failed"
        self.failures.append(message)

    def skip(self, message: str) -> None:
        if self.status == "passed":
            self.status = "skipped"
        self.artifacts["skipReason"] = message

    def record_grade(self, name: str, before: int) -> None:
        new_failures = self.failures[before:]
        if new_failures:
            self.grader_results.append(
                {"name": name, "status": "failed", "notes": "; ".join(new_failures)}
            )
        elif self.status == "skipped":
            self.grader_results.append({"name": name, "status": "skipped", "notes": "case skipped"})
        else:
            self.grader_results.append({"name": name, "status": "passed"})


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def git_sha() -> str:
    git = shutil.which("git")
    if git is None:
        return "0" * 40
    try:
        result = subprocess.run(  # noqa: S603 - fixed git executable plus fixed argv.
            [git, "rev-parse", "HEAD"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except Exception:
        return "0" * 40
    if result.returncode != 0:
        return "0" * 40
    return result.stdout.strip()


def parse_suite(path: Path) -> dict[str, Any]:
    raw = load_json(path)
    if not isinstance(raw, dict):
        raise ValueError("suite must be a JSON object")
    for key in (
        "suiteId",
        "suiteKind",
        "schemaRevision",
        "runner",
        "thresholds",
        "modeCoverage",
        "cases",
    ):
        if key not in raw:
            raise ValueError(f"suite missing {key}")
    runner = raw.get("runner")
    if not isinstance(runner, dict):
        raise ValueError("suite runner must be an object")
    for key in ("requiresNetwork", "requiresHostedProvider", "usesRealSpicetify"):
        if runner.get(key) is not False:
            raise ValueError(f"suite runner {key} must be false")
    cases = raw.get("cases")
    if not isinstance(cases, list):
        raise ValueError("suite must contain a cases array")

    fixtures = fixture_ids()
    used_fixtures: set[str] = set()
    ids: set[str] = set()
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            raise ValueError(f"case {index} must be an object")
        case_dict = cast(dict[str, Any], case)
        validate_case_shape(case_dict, index, ids, fixtures)
        ids.add(str(case_dict["id"]))
        used_fixtures.add(str(case_dict["fixture"]))

    missing = sorted(used_fixtures - fixtures)
    if missing:
        raise ValueError("suite references missing fixtures: " + ", ".join(missing))
    enforce_suite_profile(raw, cases, fixtures, used_fixtures)
    unused = sorted(fixtures - used_fixtures)
    if unused and raw.get("allowUnusedFixtures") is not True:
        raise ValueError("fixture manifests are unused by suite: " + ", ".join(unused))
    return raw


def enforce_suite_profile(
    suite: dict[str, Any],
    cases: list[Any],
    fixtures: set[str],
    used_fixtures: set[str],
) -> None:
    suite_kind = suite.get("suiteKind")
    thresholds = as_dict(suite.get("thresholds"))
    if suite_kind == "focused":
        if thresholds.get("modeCoverageRequired") is not False:
            raise ValueError("focused suite must set modeCoverageRequired=false")
        if suite.get("allowUnusedFixtures") is not True:
            raise ValueError("focused suite must set allowUnusedFixtures=true")
        return
    if suite_kind != "canonical":
        raise ValueError("suiteKind must be canonical or focused")

    if suite.get("allowUnusedFixtures") is True:
        raise ValueError("canonical suite cannot allow unused fixtures")
    if thresholds.get("modeCoverageRequired") is not True:
        raise ValueError("canonical suite must set modeCoverageRequired=true")
    required_modes = set(ALL_MODES) - {"plan"}
    declared_modes = set(suite.get("modeCoverage", []))
    if declared_modes != required_modes:
        missing = sorted(required_modes - declared_modes)
        extra = sorted(declared_modes - required_modes)
        raise ValueError(f"canonical suite modeCoverage mismatch; missing={missing}, extra={extra}")
    case_modes = {
        str(case.get("mode"))
        for case in cases
        if isinstance(case, dict) and isinstance(case.get("mode"), str)
    }
    missing_modes = sorted(required_modes - case_modes)
    if missing_modes:
        raise ValueError("canonical suite lacks cases for modes: " + ", ".join(missing_modes))
    unused = sorted(fixtures - used_fixtures)
    if unused:
        raise ValueError("canonical suite fixture manifests are unused: " + ", ".join(unused))


def validate_case_shape(
    case: dict[str, Any], index: int, ids: set[str], fixtures: set[str]
) -> None:
    required = {
        "id",
        "title",
        "prompt",
        "category",
        "mode",
        "activation",
        "fixture",
        "expected",
        "forbid",
        "text",
        "oracles",
        "traceOracle",
        "rationale",
        "source",
    }
    missing = sorted(required - set(case))
    if missing:
        raise ValueError(f"case {index} missing required fields: {', '.join(missing)}")
    case_id = case.get("id")
    if not isinstance(case_id, str) or not case_id:
        raise ValueError(f"case {index} missing id")
    if case_id in ids:
        raise ValueError(f"duplicate case id: {case_id}")
    if not isinstance(case.get("prompt"), str):
        raise ValueError(f"case {case_id} missing prompt")
    if case.get("fixture") not in fixtures:
        raise ValueError(f"case {case_id} references missing fixture {case.get('fixture')!r}")
    activation = case.get("activation")
    if not isinstance(activation, dict) or activation.get("kind") not in ACTIVATION_KINDS:
        raise ValueError(f"case {case_id} activation.kind is invalid")
    expected = case.get("expected")
    if not isinstance(expected, dict):
        raise ValueError(f"case {case_id} expected must be object")
    if activation["kind"] == "negative-trigger" and expected.get("skillActivated") is not False:
        raise ValueError(f"case {case_id} negative trigger must expect skillActivated=false")
    if activation["kind"] != "negative-trigger" and expected.get("skillActivated") is not True:
        raise ValueError(f"case {case_id} active eval must expect skillActivated=true")
    trace_oracle = case.get("traceOracle")
    if not isinstance(trace_oracle, dict):
        raise ValueError(f"case {case_id} traceOracle must be object")
    if trace_oracle.get("match") not in TRACE_MATCHES:
        raise ValueError(f"case {case_id} traceOracle.match is invalid")
    if not isinstance(trace_oracle.get("steps"), list):
        raise ValueError(f"case {case_id} traceOracle.steps must be an array")
    if "fake-execute" in expected.get("trace", []) and expected.get("executeFake") is not True:
        raise ValueError(f"case {case_id} fake-execute trace requires expected.executeFake=true")
    for key in ("reportSchemas", "outputArtifacts", "commandIds", "trace"):
        if key in expected and not isinstance(expected[key], list):
            raise ValueError(f"case {case_id} expected.{key} must be an array")
    forbid = case.get("forbid")
    if not isinstance(forbid, dict):
        raise ValueError(f"case {case_id} forbid must be object")
    for key in ("realSpicetifyBinary", "hostedEvalProvider", "unapprovedMutation"):
        if forbid.get(key) is not True:
            raise ValueError(f"case {case_id} forbid.{key} must be true")


def fixture_ids() -> set[str]:
    return {path.parent.name for path in FIXTURE_ROOT.glob("*/fixture.json")}


def load_fixture(fixture_id: str) -> dict[str, Any]:
    path = FIXTURE_ROOT / fixture_id / "fixture.json"
    data = load_json(path)
    if not isinstance(data, dict):
        raise ValueError(f"fixture {fixture_id} must be object")
    if data.get("fixtureId") != fixture_id:
        raise ValueError(f"fixture {fixture_id} fixtureId mismatch")
    if data.get("forbidLiveSpotifyMutation") is not True:
        raise ValueError(f"fixture {fixture_id} must forbid live Spotify mutation")
    return data


def case_selected(
    case: dict[str, Any], *, category: str | None, mode: str | None, case_id: str | None
) -> bool:
    if case_id and case.get("id") != case_id:
        return False
    if category and case.get("category") != category and category not in case.get("tags", []):
        return False
    expected = case.get("expected", {}) if isinstance(case.get("expected"), dict) else {}
    case_mode = expected.get("mode") or case.get("mode")
    if mode and case_mode != mode:
        return False
    return True


def run_case(case: dict[str, Any], *, fixture_root: Path, execute_fake: bool) -> CaseResult:
    case_id = str(case["id"])
    expected = case.get("expected", {}) if isinstance(case.get("expected"), dict) else {}
    forbid = case.get("forbid", {}) if isinstance(case.get("forbid"), dict) else {}
    text = case.get("text", {}) if isinstance(case.get("text"), dict) else {}
    trace_oracle = case.get("traceOracle", {}) if isinstance(case.get("traceOracle"), dict) else {}
    activation = case.get("activation", {}) if isinstance(case.get("activation"), dict) else {}
    prompt = str(case.get("prompt", ""))
    target = case.get("target")
    target_str = str(target) if target is not None else None
    fixture = load_fixture(str(case["fixture"]))
    case_root = fixture_root / f"{case_id}-{uuid.uuid4().hex}"
    materialize_fixture(fixture, case_root)
    result = CaseResult(
        case_id, str(expected.get("mode")) if expected.get("mode") else None, case.get("category")
    )
    result.artifacts["fixture"] = {
        "id": fixture["fixtureId"],
        "scenario": fixture.get("scenario"),
        "expectedFindings": fixture.get("expectedFindings", []),
    }

    before = snapshot_tree(case_root)
    trace: list[str] = ["route-mode"]
    plan: dict[str, Any]

    if activation.get("kind") == "negative-trigger":
        activated = should_activate_skill(prompt)
        plan = {
            "mode": expected.get("mode", "inspect"),
            "status": "not-activated",
            "dryRun": True,
            "mutates": False,
            "commands": [],
            "policy": {
                "risk": "blocked",
                "allowed": False,
                "requiresConfirmation": False,
                "reason": "Skill not activated for unrelated prompt",
            },
            "reason": "not activated",
        }
        if activated:
            result.fail("negative trigger activated /spicetify")
        trace.extend(["refuse", "report"])
        result.artifacts["plan"] = redacted_payload(plan)
        result.artifacts["trace"] = trace
        run_grader(result, "activation", lambda: assert_activation(result, False, expected))
        run_grader(
            result, "state", lambda: assert_state(result, before, snapshot_tree(case_root), case)
        )
        run_grader(result, "trace", lambda: assert_trace(result, trace, trace_oracle, expected))
        run_grader(
            result,
            "reports-artifacts",
            lambda: assert_reports_and_artifacts(result, plan, expected),
        )
        run_grader(result, "text", lambda: assert_text(result, plan, text))
        return result

    if not should_activate_skill(prompt):
        result.fail("active eval did not activate /spicetify")
    trace.insert(0, "activate-skill")
    requested_mode = str(case.get("mode") or expected.get("mode") or "plan")
    if activation.get("kind") == "route-mode":
        requested_mode = "plan"
    try:
        plan = plan_mode(requested_mode, prompt=prompt, target=target_str)
    except Exception as exc:
        result.fail(f"planner raised {type(exc).__name__}: {exc}")
        return result

    trace.append("dry-run-plan")
    if plan.get("policy"):
        trace.append("policy-decision")
    if plan.get("status") == "blocked":
        trace.append("refuse")
    else:
        snapshot = as_dict(plan.get("snapshot"))
        if snapshot.get("required"):
            trace.append("snapshot-gate")
        policy = as_dict(plan.get("policy"))
        if policy.get("requiresConfirmation"):
            trace.append("confirmation-gate")

    result.artifacts["plan"] = redacted_payload(plan)
    result.artifacts["plannedReportSchemas"] = planned_report_schemas(plan)
    result.artifacts["plannedArtifacts"] = planned_artifacts(plan)

    if expected.get("executeFake") is True:
        if not execute_fake:
            result.skip("case requires --execute-fake for guarded fake execution")
        else:
            fake_status = execute_plan_fake(plan, case_id, case_root, fixture)
            trace.append("fake-execute")
            if plan.get("verification"):
                trace.append("verify")
            result.artifacts["fakeExecution"] = fake_status
            if fake_status.get("status") != "verified":
                result.fail(f"fake execution was not verified: {fake_status.get('status')}")
    rollback = as_dict(plan.get("rollback"))
    if rollback.get("available"):
        trace.append("rollback-metadata")
    if plan.get("mode") == "evolve":
        trace.append("evolve-review")
    trace.append("report")
    result.artifacts["trace"] = trace
    result.artifacts["redactionProbe"] = redaction_probe(fixture)

    after_plan = snapshot_tree(case_root)
    if result.status != "skipped":
        run_grader(result, "activation", lambda: assert_activation(result, True, expected))
        run_grader(
            result, "structured-behavior", lambda: assert_expected_plan(result, plan, expected)
        )
        run_grader(result, "hard-safety", lambda: assert_forbidden(result, plan, forbid))
        run_grader(result, "state", lambda: assert_state(result, before, after_plan, case))
        run_grader(result, "trace", lambda: assert_trace(result, trace, trace_oracle, expected))
        run_grader(
            result,
            "reports-artifacts",
            lambda: assert_reports_and_artifacts(result, plan, expected),
        )
        run_grader(
            result,
            "redaction",
            lambda: assert_redaction(result, fixture, case.get("redactionOracle")),
        )
        run_grader(result, "text", lambda: assert_text(result, plan, text))

    return result


def run_grader(result: CaseResult, name: str, check: Any) -> None:
    before = len(result.failures)
    check()
    result.record_grade(name, before)


def should_activate_skill(prompt: str) -> bool:
    lowered = prompt.lower()
    if "/spicetify" in lowered:
        return True
    if "spicetify" not in lowered:
        return False
    return any(
        marker in lowered
        for marker in (
            "theme",
            "extension",
            "custom app",
            "snippet",
            "audit",
            "repair",
            "apply",
            "rollback",
            "snapshot",
            "config",
            "profile",
            "eval",
            "evolve",
        )
    )


def materialize_fixture(fixture: dict[str, Any], root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    root_resolved = root.resolve()
    entries = fixture.get("filesystem", [])
    if not isinstance(entries, list):
        raise ValueError(f"fixture {fixture.get('fixtureId')} filesystem must be an array")
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("fixture filesystem entries must be objects")
        raw_path = entry.get("path")
        if not isinstance(raw_path, str) or not raw_path:
            raise ValueError("fixture filesystem entry missing path")
        rel = Path(raw_path)
        if rel.is_absolute() or "~" in raw_path or ".." in rel.parts:
            raise ValueError(f"unsafe fixture path: {raw_path}")
        dest = root / rel
        try:
            dest.resolve().relative_to(root_resolved)
        except ValueError as exc:
            raise ValueError(f"fixture path escapes temp root: {raw_path}") from exc
        kind = str(entry.get("kind", "file"))
        if kind == "directory":
            dest.mkdir(parents=True, exist_ok=True)
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        if kind == "canary":
            content = str(entry.get("canaryValue", ""))
        else:
            content = str(entry.get("content", ""))
        dest.write_text(content, encoding="utf-8")


def assert_activation(result: CaseResult, activated: bool, expected: dict[str, Any]) -> None:
    if expected.get("skillActivated") is not activated:
        result.fail(
            f"expected skillActivated={expected.get('skillActivated')!r}, got {activated!r}"
        )


def assert_expected_plan(
    result: CaseResult, plan: dict[str, Any], expected: dict[str, Any]
) -> None:
    policy_label = expected_policy_label(plan)
    checks = {
        "mode": plan.get("mode"),
        "status": plan.get("status"),
        "dryRun": plan.get("dryRun"),
        "mutates": plan.get("mutates"),
        "policy": policy_label,
    }
    policy = plan.get("policy") if isinstance(plan.get("policy"), dict) else {}
    checks.update(
        {
            "risk": policy.get("risk") if isinstance(policy, dict) else None,
            "policyAllowed": policy.get("allowed") if isinstance(policy, dict) else None,
            "requiresConfirmation": policy.get("requiresConfirmation")
            if isinstance(policy, dict)
            else None,
        }
    )
    snapshot = plan.get("snapshot") if isinstance(plan.get("snapshot"), dict) else {}
    checks["requiresSnapshot"] = (
        bool(snapshot.get("required")) if isinstance(snapshot, dict) else False
    )
    route = plan.get("route") if isinstance(plan.get("route"), dict) else {}
    if isinstance(route, dict):
        checks.update(
            {
                "primaryIntent": route.get("primaryIntent"),
                "assetKind": route.get("assetKind"),
                "sourceKind": route.get("sourceKind"),
                "nextArtifact": route.get("nextArtifact"),
            }
        )
    for key, actual in checks.items():
        if key in expected and expected[key] != actual:
            result.fail(f"expected {key}={expected[key]!r}, got {actual!r}")
    expected_commands = expected.get("commands", expected.get("commandIds"))
    if expected_commands is not None:
        ids = command_ids(plan)
        if ids != expected_commands:
            result.fail(f"expected commands {expected_commands!r}, got {ids!r}")
    expected_any = expected.get("anyCommands")
    if expected_any:
        ids = set(command_ids(plan))
        if not ids.intersection(set(expected_any)):
            result.fail(f"expected at least one command in {expected_any!r}, got {sorted(ids)!r}")
    if expected.get("confirmationContract"):
        for required in ("planHash", "policy", "snapshot", "rollback"):
            if required not in plan:
                result.fail(f"confirmation contract missing {required}")


def assert_forbidden(result: CaseResult, plan: dict[str, Any], forbid: dict[str, Any]) -> None:
    commands = [
        cast(dict[str, Any], command)
        for command in as_list(plan.get("commands"))
        if isinstance(command, dict)
    ]
    ids = command_ids(plan)
    argv_text = " ".join(
        " ".join(str(arg) for arg in command.get("argv", [])) for command in commands
    )
    raw_payload_text = json.dumps(plan, sort_keys=True)
    redacted_text = json.dumps(redacted_payload(plan), sort_keys=True)
    structured_text = "\n".join(structured_safety_strings(plan))
    if forbid.get("commands") is True and ids:
        result.fail(f"expected no commands, got {ids!r}")
    forbidden_ids = forbid.get("commandIds", [])
    if isinstance(forbidden_ids, list):
        overlap = sorted(set(ids).intersection(str(item) for item in forbidden_ids))
        if overlap:
            result.fail(f"forbidden command ids present: {overlap}")
    shell_forbidden = bool(forbid.get("shell") or forbid.get("arbitraryShell"))
    if shell_forbidden and any(marker in argv_text for marker in SHELL_MARKERS):
        result.fail("shell metacharacter appeared in command argv")
    if shell_forbidden and any(c.get("shell") is not False for c in commands):
        result.fail("command did not explicitly set shell=false")
    if shell_forbidden and _contains_executable_text(
        structured_text,
        {"installer shell pipeline", "shell execution", "privileged filesystem command"},
    ):
        result.fail("shell execution pattern appeared in structured output")
    if forbid.get("packageManager") and contains_any(argv_text.lower(), PACKAGE_MANAGER_MARKERS):
        result.fail("package-manager command appeared in argv")
    if forbid.get("packageManager") and _contains_executable_text(
        structured_text, {"package-manager command"}
    ):
        result.fail("package-manager command appeared in structured output")
    if (forbid.get("installer") or forbid.get("installerScripts")) and contains_any(
        argv_text.lower(), INSTALLER_MARKERS
    ):
        result.fail("installer/permission command appeared in argv")
    if (forbid.get("installer") or forbid.get("installerScripts")) and _contains_executable_text(
        structured_text,
        {"installer shell pipeline", "shell execution", "privileged filesystem command"},
    ):
        result.fail("installer/permission command appeared in structured output")
    if forbid.get("network") and re.search(r"https?://", argv_text):
        result.fail("network URL appeared in argv")
    if forbid.get("realPaths") and any(
        pattern.search(raw_payload_text) for pattern in REAL_PATH_REGEXES
    ):
        result.fail("real Spotify/Spicetify path appeared in raw structured output")
    if forbid.get("secretsInOutput") and redacted_text != redact(redacted_text, strict=True):
        result.fail("unredacted secret-like value appeared in structured output")
    if forbid.get("realSpicetifyBinary") and any(
        isinstance(command, dict) and command.get("program") != "spicetify" for command in commands
    ):
        result.fail("command targeted a non-Spicetify program")
    if forbid.get("hostedEvalProvider") and contains_any(
        raw_payload_text.lower(), HOSTED_PROVIDER_MARKERS
    ):
        result.fail("hosted eval provider marker appeared in structured output")
    if forbid.get("unapprovedMutation") and bool(plan.get("mutates")):
        policy = as_dict(plan.get("policy"))
        snapshot = as_dict(plan.get("snapshot"))
        if policy.get("requiresConfirmation") is not True:
            result.fail("mutating plan did not require confirmation")
        if snapshot.get("required") is not True:
            result.fail("mutating plan did not require snapshot protection")


def assert_state(
    result: CaseResult,
    before: dict[str, str],
    after: dict[str, str],
    case: dict[str, Any],
) -> None:
    state_oracle = case.get("stateOracle")
    if state_oracle in {"no-mutation", "hash-manifest", "redaction-corpus"} and after != before:
        result.fail("planning changed fixture filesystem")
    expected = case.get("expected", {}) if isinstance(case.get("expected"), dict) else {}
    if state_oracle == "plan-hash-drift" and not expected.get("confirmationContract", True):
        result.fail("plan hash drift scenario must require confirmation contract checks")
    if state_oracle == "evolution-report" and case.get("mode") != "evolve":
        result.fail("evolution-report state oracle can only be used by evolve mode")
    if state_oracle in {"restore-exact", "rollback-exact"} and not expected.get("requiresSnapshot"):
        result.fail(f"{state_oracle} requires snapshot metadata")


def assert_trace(
    result: CaseResult,
    actual_steps: list[str],
    trace_oracle: dict[str, Any],
    expected: dict[str, Any],
) -> None:
    required = expected.get("trace", [])
    if isinstance(required, list) and required:
        missing = [step for step in required if step not in actual_steps]
        if missing:
            result.fail(f"missing expected trace steps: {missing}")

    match = trace_oracle.get("match")
    steps = trace_oracle.get("steps", [])
    if not isinstance(steps, list):
        result.fail("traceOracle.steps must be a list")
        return
    forbidden = trace_oracle.get("forbiddenSteps", [])
    if isinstance(forbidden, list):
        overlap = [step for step in forbidden if step in actual_steps]
        if overlap:
            result.fail(f"forbidden trace steps present: {overlap}")
    if match == "exact" and actual_steps != steps:
        result.fail(f"expected exact trace {steps!r}, got {actual_steps!r}")
    elif match == "contains-in-order" and not contains_in_order(actual_steps, steps):
        result.fail(f"trace does not contain required ordered steps {steps!r}: {actual_steps!r}")
    elif match == "unordered-subset":
        missing = [step for step in steps if step not in actual_steps]
        if missing:
            result.fail(f"trace missing unordered steps: {missing}")
    elif match == "forbidden":
        overlap = [step for step in steps if step in actual_steps]
        if overlap:
            result.fail(f"forbidden trace steps present: {overlap}")


def assert_reports_and_artifacts(
    result: CaseResult, plan: dict[str, Any], expected: dict[str, Any]
) -> None:
    reports = planned_report_schemas(plan)
    artifacts = planned_artifacts(plan)
    result.artifacts["plannedReportSchemas"] = reports
    result.artifacts["plannedArtifacts"] = artifacts
    for schema in expected.get("reportSchemas", []):
        if schema not in reports:
            result.fail(f"expected report schema {schema!r} was not planned")
    for artifact in expected.get("outputArtifacts", []):
        if artifact not in artifacts:
            result.fail(f"expected output artifact {artifact!r} was not planned")


def assert_text(result: CaseResult, plan: dict[str, Any], text: dict[str, Any]) -> None:
    haystack = json.dumps(redacted_payload(plan), sort_keys=True).lower()
    contains = text.get("contains", text.get("mustInclude", []))
    if isinstance(contains, list):
        for item in contains:
            if str(item).lower() not in haystack:
                result.fail(f"expected text to contain {item!r}")
    not_contains = text.get("notContains", text.get("mustNotInclude", []))
    if isinstance(not_contains, list):
        for item in not_contains:
            if str(item).lower() in haystack:
                result.fail(f"expected text not to contain {item!r}")


def assert_redaction(result: CaseResult, fixture: dict[str, Any], redaction_oracle: Any) -> None:
    payload = json.dumps(redacted_payload(result.artifacts), sort_keys=True)
    raw_artifacts = json.dumps(result.artifacts, sort_keys=True)
    canaries = fixture_canaries(fixture)
    if redaction_oracle in {"secret-corpus", "all-artifacts"}:
        leaked = [canary for canary in canaries if canary and canary in payload]
        if leaked:
            result.fail(f"redaction canaries leaked: {leaked}")
        if SYNTHETIC_SECRET_PREFIX in payload or SYNTHETIC_SECRET_PREFIX in raw_artifacts:
            result.fail("synthetic secret canary prefix leaked into artifacts")
        if raw_artifacts != redact(raw_artifacts, strict=True):
            result.fail("artifact payload contains unredacted secret-like text")
    if redaction_oracle in {"private-paths", "all-artifacts", "devtools-logs"}:
        if any(pattern.search(raw_artifacts) for pattern in REAL_PATH_REGEXES):
            result.fail("real-path canary leaked into artifacts")


def planned_report_schemas(plan: dict[str, Any]) -> list[str]:
    mode = str(plan.get("mode", ""))
    status = str(plan.get("status", ""))
    route = as_dict(plan.get("route"))
    primary_intent = str(route.get("primaryIntent", ""))
    reports = {"operation-plan"}
    if primary_intent == "research" or "research" in plan:
        reports.add("asset-analysis")
        return sorted(reports)
    if status == "blocked":
        if mode in {"audit", "extension", "custom-app", "snippet", "marketplace", "theme"}:
            reports.add("audit-report")
        return sorted(reports)
    if plan.get("commands") and bool(plan.get("mutates")):
        reports.add("operation-run")
    if plan.get("verification"):
        reports.add("verification-report")
    if mode in {"audit", "extension", "custom-app", "snippet", "marketplace", "theme"}:
        reports.add("audit-report")
    if mode in {"snapshot", "rollback"}:
        reports.add("snapshot-manifest")
    if mode in {"report", "devtools", "uninstall"}:
        reports.add("operation-report")
    if mode == "evolve":
        reports.add("evolution-report")
    return sorted(reports)


def planned_artifacts(plan: dict[str, Any]) -> list[str]:
    mode = str(plan.get("mode", ""))
    status = str(plan.get("status", ""))
    artifacts = {"redacted-report"}
    route = as_dict(plan.get("route"))
    primary_intent = str(route.get("primaryIntent", ""))
    if status != "blocked":
        artifacts.add("dry-run-plan")
    rollback = as_dict(plan.get("rollback"))
    if rollback.get("available"):
        artifacts.add("rollback-metadata")
    if mode == "snapshot":
        artifacts.add("snapshot-manifest")
    if mode in {"extension", "marketplace"} and primary_intent != "research":
        artifacts.add("provenance-lock")
    if mode == "evolve":
        artifacts.add("evolution-report")
    if primary_intent == "research" or "research" in plan:
        artifacts.add("asset-analysis")
        artifacts.add("research-report")
    return sorted(artifacts)


def redaction_probe(fixture: dict[str, Any]) -> dict[str, str]:
    raw = "\n".join(fixture_canaries(fixture))
    return {"redacted": redact(raw, strict=True)}


def fixture_canaries(fixture: dict[str, Any]) -> list[str]:
    canaries: list[str] = []
    for entry in fixture.get("filesystem", []):
        if not isinstance(entry, dict):
            continue
        if entry.get("kind") == "canary" and entry.get("mustNeverTouch") is True:
            canary_value = entry.get("canaryValue")
            if isinstance(canary_value, str):
                canaries.append(canary_value)
        for key in ("content", "canaryValue"):
            value = entry.get(key)
            if isinstance(value, str) and (
                SYNTHETIC_SECRET_PREFIX in value or any(p.search(value) for p in REAL_PATH_REGEXES)
            ):
                canaries.append(value)
    for response in fixture.get("spicetifyResponses", []):
        if not isinstance(response, dict):
            continue
        for key in ("stdout", "stderr"):
            value = response.get(key)
            if isinstance(value, str) and SYNTHETIC_SECRET_PREFIX in value:
                canaries.append(value.strip())
    return canaries


def expected_policy_label(plan: dict[str, Any]) -> str:
    if plan.get("status") in {"blocked", "not-activated"}:
        return "blocked"
    policy = plan.get("policy") if isinstance(plan.get("policy"), dict) else {}
    if not isinstance(policy, dict) or policy.get("allowed") is False:
        return "blocked"
    if policy.get("requiresConfirmation"):
        return "confirmation-required"
    if plan.get("dryRun"):
        return "dry-run-only"
    return "allowed"


def command_ids(plan: dict[str, Any]) -> list[str]:
    commands = plan.get("commands")
    if not isinstance(commands, list):
        return []
    return [
        str(command.get("id"))
        for command in commands
        if isinstance(command, dict) and command.get("id")
    ]


def contains_any(text: str, needles: tuple[str, ...]) -> bool:
    return any(needle in text for needle in needles)


def _contains_executable_text(text: str, labels: set[str]) -> bool:
    return any(
        label in labels and pattern.search(text) for label, pattern in EXECUTABLE_TEXT_REGEXES
    )


def structured_safety_strings(payload: Any, path: tuple[str, ...] = ()) -> list[str]:
    if isinstance(payload, dict):
        values: list[str] = []
        for key, value in payload.items():
            values.extend(structured_safety_strings(value, (*path, str(key))))
        return values
    if isinstance(payload, list):
        values = []
        for index, value in enumerate(payload):
            values.extend(structured_safety_strings(value, (*path, str(index))))
        return values
    if not isinstance(payload, str):
        return []
    if _allowed_metadata_url(path, payload):
        return []
    return [payload]


def _allowed_metadata_url(path: tuple[str, ...], value: str) -> bool:
    if not re.search(r"https?://", value):
        return False
    key = path[-1] if path else ""
    return key in {"locator", "url", "sourceUrl", "sourceId"} and not _contains_executable_text(
        value,
        {
            "package-manager command",
            "installer shell pipeline",
            "shell execution",
            "privileged filesystem command",
        },
    )


def contains_in_order(actual: list[str], expected: list[str]) -> bool:
    pos = 0
    for step in actual:
        if pos < len(expected) and step == expected[pos]:
            pos += 1
    return pos == len(expected)


def redacted_payload(payload: Any) -> Any:
    if isinstance(payload, dict):
        return {str(key): redacted_payload(value) for key, value in payload.items()}
    if isinstance(payload, list):
        return [redacted_payload(value) for value in payload]
    if isinstance(payload, str):
        return redact(payload, strict=True)
    return payload


def snapshot_tree(root: Path) -> dict[str, str]:
    if not root.exists():
        return {}
    result: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if path.is_file():
            try:
                rel = path.relative_to(root).as_posix()
                result[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
            except OSError:
                continue
    return result


def execute_plan_fake(
    plan: dict[str, Any], case_id: str, fixture_root: Path, fixture: dict[str, Any]
) -> dict[str, Any]:
    temp = fixture_root.parent / f"{fixture_root.name}-execution"
    temp.mkdir(parents=True, exist_ok=True)
    fake_bin = temp / "fake_spicetify.py"
    responses_file = temp / "responses.json"
    responses = {
        "\u0000".join(str(arg) for arg in response.get("argv", [])): response
        for response in fixture.get("spicetifyResponses", [])
        if isinstance(response, dict)
    }
    write_json(responses_file, responses)
    fake_bin.write_text(
        "#!/usr/bin/env python3\n"
        "import json, os, sys\n"
        "responses = json.load(open(os.environ['SPICETIFY_FAKE_RESPONSES'], encoding='utf-8'))\n"
        "argv = sys.argv[1:]\n"
        "log = os.environ.get('FAKE_SPICETIFY_LOG')\n"
        "if log:\n"
        "    with open(log, 'a', encoding='utf-8') as fh:\n"
        "        fh.write(json.dumps({'argv': argv}) + '\\n')\n"
        "fallback = {'exitCode': 127, 'stdout': '', "
        "'stderr': 'missing fake spicetify response for argv: ' + json.dumps(argv) + '\\n'}\n"
        "response = responses.get('\\u0000'.join(argv), fallback)\n"
        "sys.stdout.write(response.get('stdout', ''))\n"
        "sys.stderr.write(response.get('stderr', ''))\n"
        "raise SystemExit(int(response.get('exitCode', 0)))\n",
        encoding="utf-8",
    )
    fake_bin.chmod(0o755)
    plan_file = temp / "plan.json"
    write_json(plan_file, plan)
    state_root = temp / "state"
    log_file = temp / "argv.jsonl"
    env = {
        "PATH": os.environ.get("PATH", ""),
        "PYTHONPATH": str(SCRIPT_ROOT),
        "HOME": str(temp / "home"),
        "XDG_CONFIG_HOME": str(temp / "xdg-config"),
        "XDG_DATA_HOME": str(temp / "xdg-data"),
        "TMPDIR": str(temp),
        "SPICETIFY_AGENT_ALLOW_FAKE_BIN": "1",
        "SPICETIFY_AGENT_FAKE_BIN_ROOT": str(temp),
        "FAKE_SPICETIFY_LOG": str(log_file),
        "SPICETIFY_FAKE_RESPONSES": str(responses_file),
    }
    cmd = [
        sys.executable,
        "-m",
        "spicetify_agent",
        "--json",
        "execute-plan",
        str(plan_file),
        "--confirm",
        str(plan.get("planHash", "")),
        "--fake-bin",
        str(fake_bin),
        "--userdata-root",
        str(fixture_root),
        "--state-root",
        str(state_root),
    ]
    proc = subprocess.run(  # noqa: S603 - argv is built from repo-local fake fixtures only.
        cmd,
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )
    stdout = redact(proc.stdout, strict=True)
    stderr = redact(proc.stderr, strict=True)
    try:
        parsed = json.loads(stdout) if stdout.strip() else {}
    except json.JSONDecodeError:
        parsed = {"stdout": stdout}
    argv_log = []
    if log_file.exists():
        argv_log = [
            json.loads(line)
            for line in log_file.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
    return {
        "caseId": case_id,
        "status": parsed.get("status", "error") if proc.returncode == 0 else "error",
        "returncode": proc.returncode,
        "stdout": parsed,
        "stderr": stderr,
        "argvLog": argv_log,
    }


def build_report(
    *,
    suite: dict[str, Any],
    suite_path: Path,
    case_results: list[CaseResult],
    started_at: str,
    args: argparse.Namespace,
) -> dict[str, Any]:
    completed_at = datetime.now(UTC).isoformat()
    failures = [case for case in case_results if case.status == "failed"]
    skipped = [case for case in case_results if case.status == "skipped"]
    errors: list[CaseResult] = []
    total = len(case_results)
    passed = total - len(failures) - len(skipped) - len(errors)
    security_cases = [
        case for case in case_results if case.category in {"security", "privacy", "third-party"}
    ]
    security_failures = [case for case in security_cases if case.status == "failed"]
    blocking_total = total - len(skipped)
    security_total = len([case for case in security_cases if case.status != "skipped"])
    return {
        "runId": uuid.uuid4().hex,
        "suiteId": str(suite.get("suiteId")),
        "startedAt": started_at,
        "completedAt": completed_at,
        "gitSha": git_sha(),
        "runner": {
            "command": "python3 tools/run_skill_evals.py",
            "strict": bool(args.strict),
            "repeat": int(args.repeat),
        },
        "summary": {
            "total": total,
            "passed": passed,
            "failed": len(failures),
            "skipped": len(skipped),
            "errors": len(errors),
            "blockingPassRate": passed / blocking_total if blocking_total else 1,
            "securityPassRate": (security_total - len(security_failures)) / security_total
            if security_total
            else 1,
        },
        "caseResults": [
            {
                "caseId": case.id,
                "mode": case.mode or "",
                "category": case.category,
                "status": case.status,
                "score": 1 if case.status == "passed" else 0,
                "failureReason": "; ".join(case.failures) if case.failures else "",
                "failures": case.failures,
                "graderResults": case.grader_results or [{"name": "case", "status": case.status}],
                "artifacts": case.artifacts,
                "repeats": case.repeats,
            }
            for case in case_results
        ],
        "artifacts": {
            "json": suite_path.as_posix(),
            "markdown": "",
            "traces": [case.id for case in case_results],
        },
    }


def compare_reports(baseline: Path, candidate: Path) -> dict[str, Any]:
    base = load_json(baseline)
    cand = load_json(candidate)
    base_summary = base.get("summary", {}) if isinstance(base, dict) else {}
    cand_summary = cand.get("summary", {}) if isinstance(cand, dict) else {}
    return {
        "schemaVersion": "eval-comparison.v1",
        "baseline": baseline.as_posix(),
        "candidate": candidate.as_posix(),
        "baselineSummary": base_summary,
        "candidateSummary": cand_summary,
        "deltaPassed": int(cand_summary.get("passed", 0)) - int(base_summary.get("passed", 0)),
        "deltaFailed": int(cand_summary.get("failed", 0)) - int(base_summary.get("failed", 0)),
        "deltaSkipped": int(cand_summary.get("skipped", 0)) - int(base_summary.get("skipped", 0)),
    }


def run(args: argparse.Namespace) -> int:
    if args.compare:
        left, right = args.compare
        print(json.dumps(compare_reports(Path(left), Path(right)), indent=2, sort_keys=True))
        return 0

    suite_path = Path(args.suite)
    suite = parse_suite(suite_path)
    selected = [
        case
        for case in suite["cases"]
        if case_selected(case, category=args.category, mode=args.mode, case_id=args.id)
    ]
    if not selected:
        raise SystemExit("no eval cases selected")

    started_at = datetime.now(UTC).isoformat()
    all_results: list[CaseResult] = []
    with tempfile.TemporaryDirectory(prefix="spicetify-evals-") as tempdir:
        fixture_root = Path(tempdir)
        for case in selected:
            result = run_case(case, fixture_root=fixture_root, execute_fake=args.execute_fake)
            if args.repeat > 1:
                result.repeats = []
                for _ in range(args.repeat - 1):
                    repeated = run_case(
                        case, fixture_root=fixture_root, execute_fake=args.execute_fake
                    )
                    result.repeats.append(
                        {"status": repeated.status, "failures": repeated.failures}
                    )
                    if repeated.status == "failed":
                        result.fail(f"repeat failed: {repeated.failures}")
            all_results.append(result)
            if args.fail_fast and result.status == "failed":
                break
    report = build_report(
        suite=suite,
        suite_path=suite_path,
        case_results=all_results,
        started_at=started_at,
        args=args,
    )
    if args.output:
        write_json(Path(args.output), report)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        summary = report["summary"]
        print(
            f"skill evals: {summary['passed']}/{summary['total']} passed, "
            f"{summary['skipped']} skipped ({summary['failed']} failed)"
        )
        for case in report["caseResults"]:
            if case["status"] == "failed":
                print(f"- {case['caseId']}: {case['failures']}")
    strict_failed = bool(report["summary"]["failed"])
    if args.strict and report["summary"]["passed"] == 0 and report["summary"]["skipped"] > 0:
        strict_failed = True
        if args.json:
            print("strict mode selected only skipped cases", file=sys.stderr)
        else:
            print("- strict: selected cases were all skipped")
    return 1 if args.strict and strict_failed else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run deterministic /spicetify skill evals.")
    parser.add_argument("--suite", default="evals/spicetify-eval-suite.json")
    parser.add_argument("--category")
    parser.add_argument("--mode", choices=tuple(sorted(set(ALL_MODES) | {"evolve"})))
    parser.add_argument("--id")
    parser.add_argument("--repeat", type=int, default=1)
    parser.add_argument("--output")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--fail-fast", action="store_true")
    parser.add_argument("--execute-fake", action="store_true")
    parser.add_argument(
        "--update-goldens", action="store_true", help="reserved for future golden updates"
    )
    parser.add_argument("--compare", nargs=2, metavar=("BASELINE", "CANDIDATE"))
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.repeat < 1:
        parser.error("--repeat must be >= 1")
    if args.update_goldens:
        parser.error("--update-goldens is reserved until goldens are added")
    return run(args)


if __name__ == "__main__":
    raise SystemExit(main())
