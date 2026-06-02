from __future__ import annotations

import json
from pathlib import Path

import pytest

from spark_researcher.config import CommandSpec, MetricSpec, ProjectConfig, save_config
from spark_researcher.self_edit import (
    SELF_EDIT_APPLY_CAPABILITY_ID,
    SELF_EDIT_APPLY_TOOL_NAME,
    _apply_result_ledger_path,
    _proposal_path,
    _review_path,
    apply_proposal,
)


def _governor_decision(proposal_id: str, *, capability_id: str = SELF_EDIT_APPLY_CAPABILITY_ID) -> dict:
    action = {
        "action_id": "action:self-edit-apply",
        "capability_id": capability_id,
        "action_type": "self_evolution_apply",
    }
    authorization = {
        "schema_version": "authorization-decision-v1",
        "decision_id": "decision:self-edit-apply",
        "created_at": "2026-06-02T00:00:00+00:00",
        "turn_id": "turn:self-edit-apply",
        "action_id": action["action_id"],
        "capability_id": capability_id,
        "verdict": "allow",
        "risk_tier": "high",
        "reasons": ["Explicit owner approval for self-edit apply."],
        "evidence": [
            {
                "id": "evidence:self-edit-proposal",
                "kind": "human_confirmation",
                "source": "test",
                "summary": f"Owner approved self-edit proposal {proposal_id}.",
                "confidence": 1.0,
            }
        ],
        "approval": {
            "required": True,
            "status": "approved",
            "approval_ref": {
                "id": "evidence:self-edit-human-approval",
                "kind": "human_confirmation",
                "source": "test",
                "summary": f"Approved proposal {proposal_id}.",
                "confidence": 1.0,
            },
        },
        "restrictions": [],
        "trace": {"id": "trace:self-edit-authorization", "redaction_class": "metadata_only"},
    }
    ledger = {
        "schema_version": "tool-call-ledger-v1",
        "ledger_id": "ledger:self-edit-apply",
        "created_at": "2026-06-02T00:00:00+00:00",
        "turn_id": "turn:self-edit-apply",
        "action_id": action["action_id"],
        "capability_id": capability_id,
        "tool_name": SELF_EDIT_APPLY_TOOL_NAME,
        "lifecycle": [
            {"stage": "propose", "at": "2026-06-02T00:00:00+00:00", "verdict": "passed"},
            {"stage": "authorize", "at": "2026-06-02T00:00:00+00:00", "verdict": "passed"},
            {"stage": "execute", "at": "2026-06-02T00:00:00+00:00", "verdict": "pending"},
        ],
        "authorization": authorization,
        "arguments": {
            "schema_valid": True,
            "raw_ref": {
                "id": "artifact:self-edit-raw-args",
                "kind": "self_edit_proposal",
                "path_or_uri": f"proposal:{proposal_id}",
                "redaction_class": "metadata_only",
            },
            "sanitized_ref": {
                "id": "artifact:self-edit-sanitized-args",
                "kind": "self_edit_proposal",
                "path_or_uri": f"proposal:{proposal_id}",
                "redaction_class": "metadata_only",
            },
        },
        "result": {
            "status": "not_started",
            "summary": f"Self-edit proposal {proposal_id} is authorized but not applied yet.",
            "sanitized_output_ref": {
                "id": "artifact:self-edit-not-started",
                "kind": "tool_output",
                "path_or_uri": f"proposal:{proposal_id}",
                "redaction_class": "metadata_only",
            },
        },
        "trace": {"id": "trace:self-edit-pre-ledger", "redaction_class": "metadata_only"},
    }
    return {
        "schema_version": "governor-decision-v1",
        "decision_id": "governor-decision:self-edit-apply",
        "created_at": "2026-06-02T00:00:00+00:00",
        "surface": "cli",
        "turn_id": "turn:self-edit-apply",
        "selected_move": "execute_action",
        "authority_state": "executable",
        "risk_tier": "high",
        "outcome": "execute",
        "envelope": {
            "schema_version": "turn-intent-envelope-vnext",
            "turn_id": "turn:self-edit-apply",
            "surface": "cli",
            "selected_move": "execute_action",
            "action_authority": {"state": "executable"},
            "proposed_actions": [action],
        },
        "authorizations": [authorization],
        "tool_ledgers": [ledger],
        "execution_boundary": {
            "action_authorized": True,
            "action_count": 1,
            "authorized_action_count": 1,
            "requires_human_confirmation": True,
            "legacy_authority_demoted": True,
            "reasons": ["Governor authorized self-edit apply."],
        },
        "reply_contract": {
            "style": "compact_status",
            "instruction": "Apply the reviewed self-edit proposal.",
            "inspect_link_allowed": True,
            "should_interrupt": False,
        },
        "evidence": [
            {
                "id": "evidence:self-edit-governor-proposal",
                "kind": "human_confirmation",
                "source": "test",
                "summary": f"Governor decision is bound to proposal {proposal_id}.",
                "confidence": 1.0,
            }
        ],
        "trace": {"id": "trace:self-edit-governor", "redaction_class": "metadata_only"},
    }


def _write_self_edit_fixture(repo_root: Path, proposal_id: str) -> tuple[Path, Path]:
    repo_root.mkdir(parents=True, exist_ok=True)
    config_path = repo_root / "spark-researcher.project.json"
    save_config(
        config_path,
        ProjectConfig(
            project_name="self-edit-test",
            project_root=".",
            eval_metric="score",
            eval_goal="maximize",
            commands={"research": CommandSpec(args=["python", "-c", "print('noop')"])},
            metrics={"score": MetricSpec(pattern=r"^score:\s+([0-9.]+)$")},
        ),
    )
    target = repo_root / "README.md"
    target.write_text("old\n", encoding="utf-8")
    workspace_root = repo_root / "proposal-workspace"
    workspace_root.mkdir()
    (workspace_root / "README.md").write_text("new\n", encoding="utf-8")
    proposal = {
        "proposal_id": proposal_id,
        "status": "reviewed",
        "change_count": 1,
        "blocked_changes": [],
        "allowed_changes": [{"path": "README.md", "status": "modified"}],
        "workspace_root": str(workspace_root),
    }
    proposal_path = _proposal_path(repo_root, proposal_id)
    proposal_path.parent.mkdir(parents=True, exist_ok=True)
    proposal_path.write_text(json.dumps(proposal, indent=2) + "\n", encoding="utf-8")
    review_path = _review_path(repo_root, proposal_id)
    review_path.parent.mkdir(parents=True, exist_ok=True)
    review_path.write_text(
        json.dumps({"decision": "approve", "lineage_failures": ["a", "b", "c"]}, indent=2) + "\n",
        encoding="utf-8",
    )
    return config_path, target


def test_apply_proposal_checks_remote_before_copy(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    proposal_id = "proposal-1"
    config_path, target = _write_self_edit_fixture(tmp_path / "repo", proposal_id)

    monkeypatch.setattr("spark_researcher.self_edit.run_git_status", lambda repo_root: False)
    monkeypatch.setattr("spark_researcher.self_edit._current_branch", lambda repo_root: "main")
    monkeypatch.setattr("spark_researcher.self_edit._remote_exists", lambda repo_root: False)

    with pytest.raises(RuntimeError, match="origin"):
        apply_proposal(
            config_path,
            proposal_id,
            git_mode_override="main",
            push_override=True,
            governor_decision=_governor_decision(proposal_id),
        )

    assert target.read_text(encoding="utf-8") == "old\n"
    proposal = json.loads(_proposal_path(tmp_path / "repo", proposal_id).read_text(encoding="utf-8"))
    assert proposal["status"] == "reviewed"
    assert "applied_at" not in proposal


def test_apply_proposal_records_push_failure_state(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    proposal_id = "proposal-2"
    repo_root = tmp_path / "repo"
    config_path, target = _write_self_edit_fixture(repo_root, proposal_id)

    monkeypatch.setattr("spark_researcher.self_edit.run_git_status", lambda repo_root: False)
    monkeypatch.setattr("spark_researcher.self_edit._current_branch", lambda repo_root: "main")
    monkeypatch.setattr("spark_researcher.self_edit._remote_exists", lambda repo_root: True)
    monkeypatch.setattr("spark_researcher.self_edit._commit_paths", lambda repo_root, paths, message: "abc123")

    def _raise_push(repo_root: Path, branch_name: str, remote_name: str = "origin") -> None:
        raise RuntimeError("push broke")

    monkeypatch.setattr("spark_researcher.self_edit._push_branch", _raise_push)

    with pytest.raises(RuntimeError, match="push broke"):
        apply_proposal(
            config_path,
            proposal_id,
            git_mode_override="main",
            push_override=True,
            governor_decision=_governor_decision(proposal_id),
        )

    assert target.read_text(encoding="utf-8") == "new\n"
    proposal = json.loads(_proposal_path(repo_root, proposal_id).read_text(encoding="utf-8"))
    assert proposal["status"] == "applied_push_failed"
    assert proposal["git_commit_sha"] == "abc123"
    assert proposal["git_pushed"] is False
    assert proposal["apply_error"] == "push broke"
    assert proposal["authority"]["schema_version"] == "governor-decision-v1"
    assert proposal["apply_result_status"] == "failure"
    ledger = json.loads(_apply_result_ledger_path(repo_root, proposal_id).read_text(encoding="utf-8"))
    assert ledger["schema_version"] == "tool-call-ledger-v1"
    assert ledger["result"]["status"] == "failure"


def test_apply_proposal_requires_governor_before_copy(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    proposal_id = "proposal-3"
    config_path, target = _write_self_edit_fixture(tmp_path / "repo", proposal_id)
    monkeypatch.setattr("spark_researcher.self_edit.run_git_status", lambda repo_root: False)

    with pytest.raises(RuntimeError, match="GovernorDecisionV1"):
        apply_proposal(config_path, proposal_id, git_mode_override="manual")

    assert target.read_text(encoding="utf-8") == "old\n"


def test_apply_proposal_rejects_governor_for_another_proposal(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    proposal_id = "proposal-4"
    config_path, target = _write_self_edit_fixture(tmp_path / "repo", proposal_id)
    monkeypatch.setattr("spark_researcher.self_edit.run_git_status", lambda repo_root: False)

    with pytest.raises(RuntimeError, match="proposal_id_not_bound"):
        apply_proposal(config_path, proposal_id, git_mode_override="manual", governor_decision=_governor_decision("other-proposal"))

    assert target.read_text(encoding="utf-8") == "old\n"


def test_apply_proposal_records_success_result_ledger(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    proposal_id = "proposal-5"
    repo_root = tmp_path / "repo"
    config_path, target = _write_self_edit_fixture(repo_root, proposal_id)
    monkeypatch.setattr("spark_researcher.self_edit.run_git_status", lambda repo_root: False)
    monkeypatch.setattr("spark_researcher.self_edit._current_branch", lambda repo_root: "main")

    result = apply_proposal(config_path, proposal_id, git_mode_override="manual", governor_decision=_governor_decision(proposal_id))

    assert target.read_text(encoding="utf-8") == "new\n"
    assert result["applied_files"] == ["README.md"]
    proposal = json.loads(_proposal_path(repo_root, proposal_id).read_text(encoding="utf-8"))
    assert proposal["authority"]["decision_id"] == "governor-decision:self-edit-apply"
    assert proposal["apply_result_status"] == "success"
    ledger = json.loads(_apply_result_ledger_path(repo_root, proposal_id).read_text(encoding="utf-8"))
    assert ledger["schema_version"] == "tool-call-ledger-v1"
    assert ledger["tool_name"] == SELF_EDIT_APPLY_TOOL_NAME
    assert ledger["result"]["status"] == "success"
