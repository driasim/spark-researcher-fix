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
