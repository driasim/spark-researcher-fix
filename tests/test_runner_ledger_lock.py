from __future__ import annotations

from pathlib import Path

from spark_researcher.runner import append_jsonl, locked_file, read_jsonl


def test_append_jsonl_uses_transient_lock_file(tmp_path: Path) -> None:
    path = tmp_path / "ledger" / "runs.jsonl"

    append_jsonl(path, {"run_id": "one", "metric_value": 1})
    append_jsonl(path, {"run_id": "two", "metric_value": 2})

    assert [row["run_id"] for row in read_jsonl(path)] == ["one", "two"]
    assert not path.with_name(path.name + ".lock").exists()


def test_locked_file_times_out_when_lock_is_held(tmp_path: Path) -> None:
    path = tmp_path / "ledger" / "runs.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.with_name(path.name + ".lock").write_text("held", encoding="utf-8")

    try:
        with locked_file(path, timeout_seconds=0):
            raise AssertionError("lock should not be acquired")
    except TimeoutError as exc:
        assert "runs.jsonl.lock" in str(exc)
