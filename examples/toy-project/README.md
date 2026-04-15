# Toy Project

This is a tiny deterministic target for Spark Researcher.

- `train.py` reads `config.json`
- it prints `val_loss` and `training_seconds`
- the optimum is near `learning_rate=0.0003` and `weight_decay=0.02`
- `trainer.py` simulates a DSPy-style compile trigger from `training_examples.jsonl`

## Why This Exists

The root repo ships with a config that already points at this toy project.

That means you can try Spark Researcher immediately without wiring your own project first.

## Fast Walkthrough

From the `spark-researcher` repo root:

```powershell
python -m pip install -e .
spark-researcher run --command train
spark-researcher autoloop --command train --rounds 3 --suggest-limit 3
spark-researcher memory sync
spark-researcher obsidian build
spark-researcher summary
```

## What To Expect

The default `config.json` starts at:

- `learning_rate = 0.001`
- `weight_decay = 0.01`

So the first direct run should print something close to:

```text
val_loss: 1.540000
training_seconds: 5.0
```

As `autoloop` explores better candidates, lower `val_loss` values should appear in the ledger.

## Files You Will See

After the walkthrough, the main generated outputs are:

- `artifacts/ledger.jsonl`: immutable run history
- `artifacts/memory/`: exported memory docs after `memory sync`
- `obsidian-vault/`: generated watchtower pages after `obsidian build`

## How To Read The Outcome

- lower `val_loss` is better
- the optimum is near `learning_rate=0.0003`
- the optimum is also near `weight_decay=0.02`
- large deviations from those values should score worse

## Next Step

Once this toy project makes sense, replace the bundled config target with your own project command and metric.
