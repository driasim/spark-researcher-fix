from __future__ import annotations

import json
from contextlib import contextmanager
from pathlib import Path

import pytest

from spark_researcher import candidates, runner
from spark_researcher.config import load_config
from spark_researcher.outcomes import load_advisory_outcomes
from spark_researcher.paths import ledger_path
from spark_researcher.tracing import start_trace, trace_status


def _write_ledger(runtime_root: Path, rows: list[dict]) -> None:
    path = ledger_path(runtime_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")


def test_best_metric_ignores_failed_rows(tmp_path: Path) -> None:
    runtime_root = tmp_path
    _write_ledger(
        runtime_root,
        [
            {"command_name": "research", "status": "ok", "metric_value": 1.0, "applied_mutations": []},
            {"command_name": "research", "status": "failed", "metric_value": 9.0, "applied_mutations": [{"name": "x", "value": "9"}]},
            {"command_name": "research", "status": "ok", "metric_value": 5.0, "applied_mutations": [{"name": "x", "value": "5"}]},
        ],
    )

    assert runner.best_metric(runtime_root, "research", "maximize") == 5.0


def test_baseline_metric_only_uses_ok_baseline_rows(tmp_path: Path) -> None:
    runtime_root = tmp_path
    _write_ledger(
        runtime_root,
        [
            {"command_name": "research", "status": "ok", "metric_value": 0.6, "applied_mutations": []},
            {"command_name": "research", "status": "ok", "metric_value": 0.95, "applied_mutations": [{"name": "mode", "value": "candidate"}]},
            {"command_name": "research", "status": "failed", "metric_value": 0.99, "applied_mutations": []},
        ],
    )

    assert runner.baseline_metric(runtime_root, "research", "maximize") == 0.6


def test_candidate_primitive_selection_ignores_failed_rows() -> None:
    rows = [
        {"command_name": "research", "status": "ok", "metric_value": 1.0, "applied_mutations": []},
        {
            "command_name": "research",
            "status": "failed",
            "metric_value": 9.0,
            "verdict": "improved",
            "candidate_id": "bad",
            "applied_mutations": [{"name": "lane", "value": "bad"}],
        },
        {
            "command_name": "research",
            "status": "ok",
            "metric_value": 2.0,
            "verdict": "improved",
            "candidate_id": "good",
            "applied_mutations": [{"name": "lane", "value": "good"}],
        },
    ]

    best = candidates._best_single_primitives(rows, "research", "maximize", baseline_metric=1.0)

    assert best == {
        "lane": {
            "name": "lane",
            "value": "good",
            "metric_value": 2.0,
            "candidate_id": "good",
            "reason": "beats baseline",
        }
    }


def test_candidate_ids_do_not_collapse_decimal_values() -> None:
    assert candidates._candidate_id({"learning_rate": "1.5"}) != candidates._candidate_id({"learning_rate": "15"})
    assert candidates._candidate_id({"learning_rate": "1.5"}) != candidates._candidate_id({"learning_rate": "1_dot_5"})


def test_failed_and_unknown_rows_count_as_discards() -> None:
    assert runner.row_counts_as_discard({"status": "failed", "verdict": "baseline"}) is True
    assert runner.row_counts_as_discard({"status": "ok", "verdict": "unknown"}) is True
    assert runner.row_counts_as_discard({"status": "ok", "verdict": "regressed"}) is True
    assert runner.row_counts_as_discard({"status": "ok", "verdict": "improved"}) is False

    assert candidates._row_counts_as_discard({"status": "failed", "verdict": "baseline"}) is True
    assert candidates._row_counts_as_discard({"status": "ok", "verdict": "unknown"}) is True
    assert candidates._row_counts_as_discard({"status": "ok", "verdict": "regressed"}) is True
    assert candidates._row_counts_as_discard({"status": "ok", "verdict": "improved"}) is False


def test_advisory_outcomes_skip_malformed_jsonl_rows(tmp_path: Path) -> None:
    path = tmp_path / "artifacts" / "advisory" / "outcomes.jsonl"
    path.parent.mkdir(parents=True)
    path.write_text(
        "\n".join(
            [
                json.dumps({"status": "ok", "packet_ids": ["packet-a"]}),
                "{not-json",
                json.dumps(["not", "an", "object"]),
                json.dumps({"status": "fail", "packet_ids": ["packet-b"]}),
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    rows = load_advisory_outcomes(tmp_path)

    assert [row["status"] for row in rows] == ["ok", "fail"]


def test_trace_status_skips_malformed_jsonl_rows(tmp_path: Path) -> None:
    recorder = start_trace(tmp_path, kind="advisory_research", name="retry")
    recorder.event("citation_check", attributes={"used_note_ids": ["a"], "relevant_note_ids": ["b"]})
    recorder.finish()
    index_path = tmp_path / "artifacts" / "traces" / "index.jsonl"
    trace_path = recorder.path
    index_path.write_text(index_path.read_text(encoding="utf-8") + "{not-json\n", encoding="utf-8")
    trace_path.write_text(trace_path.read_text(encoding="utf-8") + "{not-json\n", encoding="utf-8")

    status = trace_status(tmp_path)

    assert status["trace_count"] == 1
    assert status["research_signals"]["research_retry_count"] == 1
    assert status["research_signals"]["citation_check_count"] == 1
    assert status["research_signals"]["citation_mismatch_count"] == 1


def test_trace_appends_use_locked_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    locked_paths: list[Path] = []

    @contextmanager
    def fake_lock(path: Path):
        locked_paths.append(path)
        yield

    monkeypatch.setattr("spark_researcher.runner.locked_file", fake_lock)

    recorder = start_trace(tmp_path, kind="advisory_research", name="retry")
    recorder.event("citation_check")

    assert locked_paths == [recorder.path, tmp_path / "artifacts" / "traces" / "index.jsonl", recorder.path]


def test_load_config_falls_back_for_invalid_optional_numeric_values(tmp_path: Path) -> None:
    config_path = tmp_path / "spark-researcher.project.json"
    config_path.write_text(
        json.dumps(
            {
                "project_name": "demo",
                "eval_metric": "score",
                "commands": {"research": {"args": ["python", "-c", "print('ok')"]}},
                "metrics": {"score": {"pattern": "score=(?P<value>\\d+)"}},
                "trainers": [
                    {
                        "name": "writer",
                        "examples_path": "examples.jsonl",
                        "compile_command": ["python", "compile.py"],
                        "min_examples": "many",
                        "recompile_every": None,
                        "max_examples": "all",
                    }
                ],
                "guardrails": {
                    "max_loop_iterations": "forever",
                    "consecutive_discard_limit": None,
                    "near_best_tolerance": "close",
                },
            }
        )
        + "\n",
        encoding="utf-8",
    )

    config = load_config(config_path)

    assert config.trainers[0].min_examples == 20
    assert config.trainers[0].recompile_every == 10
    assert config.trainers[0].max_examples == 96
    assert config.guardrails.max_loop_iterations == 8
    assert config.guardrails.consecutive_discard_limit == 3
    assert config.guardrails.near_best_tolerance == 0.03
