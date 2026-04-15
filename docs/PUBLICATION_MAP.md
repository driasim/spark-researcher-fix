# Publication Map

This document defines the safe documentation split for publishing Spark Researcher without losing agent/operator understanding.

This is a logical archive map for now.
Files stay in place so links, agent context, Spark Swarm references, and operator habits do not regress.

## Must Stay Public

These documents form the public operating surface and should remain easy to find:

- [`README.md`](../README.md)
- [`docs/README.md`](README.md)
- [`docs/ARCHITECTURE.md`](ARCHITECTURE.md)
- [`docs/RULES.md`](RULES.md)
- [`docs/AUTOLOOP.md`](AUTOLOOP.md)
- [`docs/ADVISORY.md`](ADVISORY.md)
- [`docs/MEMORY.md`](MEMORY.md)
- [`docs/OBSIDIAN.md`](OBSIDIAN.md)
- [`docs/SELF_EDITING.md`](SELF_EDITING.md)
- [`docs/AGENT_BACKENDS.md`](AGENT_BACKENDS.md)
- [`docs/PRESETS.md`](PRESETS.md)
- [`docs/CHIPS.md`](CHIPS.md)
- [`docs/CHIP_AUTHORING.md`](CHIP_AUTHORING.md)
- [`docs/CHIP_SYSTEMS.md`](CHIP_SYSTEMS.md)
- [`docs/CHIP_VALIDATION.md`](CHIP_VALIDATION.md)

These are the minimum docs needed for a new reader or agent to understand:

- what Spark Researcher is
- how the runtime works
- how Spark Swarm connects to it
- how domain chips connect to it
- how to design a usable chip with an LLM
- how memory and Obsidian fit in
- how self-editing and advisory work

## Keep As Reference

These docs are important and should remain available, but they do not need to sit on the public front door:

- [`docs/CHECKLOOP.md`](CHECKLOOP.md)
- [`docs/RELIABILITY_TEST_PLAN.md`](RELIABILITY_TEST_PLAN.md)
- [`docs/INTENT.md`](INTENT.md)
- [`docs/CHIP_INTELLIGENCE_CONTRACT.md`](CHIP_INTELLIGENCE_CONTRACT.md)
- [`docs/CHIP_INTELLIGENCE_ROLLOUT.md`](CHIP_INTELLIGENCE_ROLLOUT.md)
- [`docs/CHIP_MEMORY_ROLLOUT.md`](CHIP_MEMORY_ROLLOUT.md)
- [`docs/CHIP_ONE_LOOP_FLYWHEEL.md`](CHIP_ONE_LOOP_FLYWHEEL.md)
- [`docs/CHIP_RESEARCH_PACKET_SCHEMA.md`](CHIP_RESEARCH_PACKET_SCHEMA.md)
- [`docs/CHIP_TAGGING_RULESET.md`](CHIP_TAGGING_RULESET.md)
- [`docs/CHIP_RESEARCH_QUALITY_RULESET.md`](CHIP_RESEARCH_QUALITY_RULESET.md)
- [`docs/CHIP_DSPY_METHOD.md`](CHIP_DSPY_METHOD.md)
- [`docs/CHIP_BENCHMARK_BRIDGE_GUIDE.md`](CHIP_BENCHMARK_BRIDGE_GUIDE.md)
- [`docs/STARTUP_BENCH_PROMOTION_BRIDGE.md`](STARTUP_BENCH_PROMOTION_BRIDGE.md)
- [`docs/CHIP_REGISTRY.md`](CHIP_REGISTRY.md)
- [`docs/MASTER_CHIP_ARCHITECT_PROMPT.md`](MASTER_CHIP_ARCHITECT_PROMPT.md)
- [`docs/master_chip_v2/README.md`](master_chip_v2/README.md)

These are primarily for:

- agent implementation quality
- deeper operator work
- chip design and review
- regression prevention

## Archive From Public Navigation

These docs can be treated as archive/internal/deep-background material for publishing purposes.
They now belong under [`docs/archive/`](archive/README.md) unless a runtime contract still depends on the original path:

- [`docs/archive/CHIP_ECOSYSTEM_HARDENING_PLAN.md`](archive/CHIP_ECOSYSTEM_HARDENING_PLAN.md)
- [`docs/archive/EXTERNAL_CHIP_TASKS.md`](archive/EXTERNAL_CHIP_TASKS.md)
- [`docs/archive/CHIP_REMEDIATION_PROMPTS.md`](archive/CHIP_REMEDIATION_PROMPTS.md)
- [`docs/archive/AI_LAB_MAP.md`](archive/AI_LAB_MAP.md)
- [`docs/archive/FRONTIER_LAB_BENCHMARKING_BOOK.md`](archive/FRONTIER_LAB_BENCHMARKING_BOOK.md)
- [`docs/archive/book-of-ai-intelligence/README.md`](archive/book-of-ai-intelligence/README.md)
- `docs/archive/book-of-ai-intelligence/*`
- `docs/archive/testing-chip/*`

These are useful context, but they are not required to understand or operate the core public system safely.

`docs/beliefs/*` is intentionally not moved yet because the runtime and watchtower system still treat it as a live output path.

## No-Regression Guardrail

Do not archive away the only copy of:

- Spark Swarm runtime-core semantics
- chip runtime contract
- memory-tier semantics
- Obsidian/watchtower semantics
- advisory/research/verifier boundary
- self-edit/backend boundaries

Those are core system semantics, not optional background reading.

## Current Policy

For now:

- keep the files where they are
- reduce front-door links to the "must stay public" set
- keep the "reference" set linked from docs for agents and advanced operators
- stop linking the "archive" set from public entry docs unless a reader is explicitly looking for deep background
