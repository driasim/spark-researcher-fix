from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Callable


ADVISORY_EXECUTE_TOOL_NAME = "researcher.advisory.execute"
ADVISORY_EXECUTE_OWNER_SYSTEM = "spark-researcher"
ADVISORY_EXECUTE_MUTATION_CLASS = "external_network"
ADVISORY_EXECUTE_ACTION_TYPE = "external_api_call"
ADVISORY_EXECUTE_CAPABILITY_ID = f"capability:{ADVISORY_EXECUTE_OWNER_SYSTEM}:{ADVISORY_EXECUTE_TOOL_NAME}"

MEMORY_WRITE_TOOL_NAME = "memory.write"
MEMORY_WRITE_OWNER_SYSTEM = "domain-chip-memory"
MEMORY_WRITE_MUTATION_CLASS = "writes_memory"
MEMORY_WRITE_ACTION_TYPE = "write_memory"
MEMORY_WRITE_CAPABILITY_ID = f"capability:{MEMORY_WRITE_OWNER_SYSTEM}:{MEMORY_WRITE_TOOL_NAME}"

CHIP_CREATE_TOOL_NAME = "researcher.chip.create"
CHIP_CREATE_OWNER_SYSTEM = "spark-researcher"
CHIP_CREATE_MUTATION_CLASS = "creates_chip"
CHIP_CREATE_ACTION_TYPE = "create_domain_chip"
CHIP_CREATE_CAPABILITY_ID = f"capability:{CHIP_CREATE_OWNER_SYSTEM}:{CHIP_CREATE_TOOL_NAME}"

RUN_EXECUTION_TOOL_NAME = "researcher.run"
RUN_EXECUTION_OWNER_SYSTEM = "spark-researcher"
RUN_EXECUTION_MUTATION_CLASS = "writes_files"
RUN_EXECUTION_ACTION_TYPE = "edit_file"
RUN_EXECUTION_CAPABILITY_ID = f"capability:{RUN_EXECUTION_OWNER_SYSTEM}:{RUN_EXECUTION_TOOL_NAME}"


def _harness_core_source_candidates() -> list[Path]:
    candidates: list[Path] = []
    candidates.append(Path(__file__).resolve().parents[3] / "spark-harness-core" / "src")
    spark_home = os.environ.get("SPARK_HOME")
    if spark_home:
        candidates.append(Path(spark_home).expanduser() / "modules" / "spark-harness-core" / "source" / "src")
    candidates.append(Path.home() / ".spark" / "modules" / "spark-harness-core" / "source" / "src")
    return candidates


def _load_verify_governor_tool_authority() -> Callable[..., dict[str, Any]]:
    try:
        from spark_harness_core.legacy_turn_intent import verify_governor_tool_authority

        return verify_governor_tool_authority
    except ModuleNotFoundError:
        pass

    for candidate in _harness_core_source_candidates():
        if not (candidate / "spark_harness_core" / "__init__.py").exists():
            continue
        candidate_text = str(candidate)
        if candidate_text not in sys.path:
            sys.path.insert(0, candidate_text)
        try:
            from spark_harness_core.legacy_turn_intent import verify_governor_tool_authority

            return verify_governor_tool_authority
        except ModuleNotFoundError:
            continue
    raise RuntimeError("spark_harness_core_unavailable")


def require_advisory_execution_authority(
    governor_decision: dict[str, Any] | None,
    *,
    action_id: str | None = None,
) -> dict[str, Any]:
    verifier = _load_verify_governor_tool_authority()
    verification = verifier(
        governor_decision,
        tool_name=ADVISORY_EXECUTE_TOOL_NAME,
        owner_system=ADVISORY_EXECUTE_OWNER_SYSTEM,
        mutation_class=ADVISORY_EXECUTE_MUTATION_CLASS,
        external_network=True,
        action_id=action_id,
        require_pre_execution_ledger=True,
    )
    if not verification.get("allowed"):
        reasons = [str(item) for item in verification.get("reason_codes", []) if str(item).strip()]
        reason_text = ", ".join(reasons) if reasons else "governor_authority_denied"
        raise RuntimeError("Advisory execution requires GovernorDecisionV1 authority: " + reason_text)
    return verification


def require_memory_write_authority(
    governor_decision: dict[str, Any] | None,
    *,
    action_id: str | None = None,
) -> dict[str, Any]:
    verifier = _load_verify_governor_tool_authority()
    verification = verifier(
        governor_decision,
        tool_name=MEMORY_WRITE_TOOL_NAME,
        owner_system=MEMORY_WRITE_OWNER_SYSTEM,
        mutation_class=MEMORY_WRITE_MUTATION_CLASS,
        action_id=action_id,
        require_pre_execution_ledger=True,
    )
    if not verification.get("allowed"):
        reasons = [str(item) for item in verification.get("reason_codes", []) if str(item).strip()]
        reason_text = ", ".join(reasons) if reasons else "governor_authority_denied"
        raise RuntimeError("Memory materialization requires GovernorDecisionV1 memory-write authority: " + reason_text)
    return verification


def require_chip_create_authority(
    governor_decision: dict[str, Any] | None,
    *,
    action_id: str | None = None,
) -> dict[str, Any]:
    verifier = _load_verify_governor_tool_authority()
    verification = verifier(
        governor_decision,
        tool_name=CHIP_CREATE_TOOL_NAME,
        owner_system=CHIP_CREATE_OWNER_SYSTEM,
        mutation_class=CHIP_CREATE_MUTATION_CLASS,
        action_id=action_id,
        require_pre_execution_ledger=True,
    )
    if not verification.get("allowed"):
        reasons = [str(item) for item in verification.get("reason_codes", []) if str(item).strip()]
        reason_text = ", ".join(reasons) if reasons else "governor_authority_denied"
        raise RuntimeError("Chip creation requires GovernorDecisionV1 chip-create authority: " + reason_text)
    return verification


def _matching_action_args_path(
    governor_decision: dict[str, Any] | None,
    *,
    capability_id: str,
    action_type: str,
    args_path: str,
    action_id: str | None = None,
) -> bool:
    envelope = governor_decision.get("envelope") if isinstance(governor_decision, dict) else {}
    proposed_actions = envelope.get("proposed_actions") if isinstance(envelope, dict) else []
    if not isinstance(proposed_actions, list):
        return False
    for action in proposed_actions:
        if not isinstance(action, dict):
            continue
        if action.get("capability_id") != capability_id:
            continue
        if action.get("action_type") != action_type:
            continue
        if action_id is not None and str(action.get("action_id") or "") != action_id:
            continue
        args_ref = action.get("args_ref") if isinstance(action.get("args_ref"), dict) else {}
        if str(args_ref.get("path_or_uri") or "") == args_path:
            return True
    return False


def require_run_execution_authority(
    governor_decision: dict[str, Any] | None,
    *,
    args_path: str,
    action_id: str | None = None,
) -> dict[str, Any]:
    verifier = _load_verify_governor_tool_authority()
    verification = verifier(
        governor_decision,
        tool_name=RUN_EXECUTION_TOOL_NAME,
        owner_system=RUN_EXECUTION_OWNER_SYSTEM,
        mutation_class=RUN_EXECUTION_MUTATION_CLASS,
        action_id=action_id,
        require_pre_execution_ledger=True,
    )
    if verification.get("allowed") and not _matching_action_args_path(
        governor_decision,
        capability_id=RUN_EXECUTION_CAPABILITY_ID,
        action_type=RUN_EXECUTION_ACTION_TYPE,
        args_path=args_path,
        action_id=action_id,
    ):
        verification = {**verification, "allowed": False, "reason_codes": ["governor_action_args_path_mismatch"]}
    if not verification.get("allowed"):
        reasons = [str(item) for item in verification.get("reason_codes", []) if str(item).strip()]
        reason_text = ", ".join(reasons) if reasons else "governor_authority_denied"
        raise RuntimeError("Researcher run requires GovernorDecisionV1 run authority: " + reason_text)
    return verification
