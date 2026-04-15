# Chip Systems

Spark currently supports two chip design systems.

This is intentional for now.

Do not treat this as two different runtime contracts.
There is one kernel-facing chip contract in [`docs/CHIPS.md`](CHIPS.md).
The choice here is about how you design and standardize a chip repo before or during implementation.

## The Shared Rule

Both systems must still satisfy:

- the runtime contract in [`docs/CHIPS.md`](CHIPS.md)
- the validation path in [`docs/CHIP_VALIDATION.md`](CHIP_VALIDATION.md)
- the Spark Swarm/runtime boundary in [`docs/ARCHITECTURE.md`](ARCHITECTURE.md)
- the watchtower contract in [`docs/OBSIDIAN.md`](OBSIDIAN.md)

## v1

Use [`docs/MASTER_CHIP_ARCHITECT_PROMPT.md`](MASTER_CHIP_ARCHITECT_PROMPT.md) when you want the older, simpler, single-prompt chip design surface.

Use `v1` when:

- you want a lighter planning pass
- you are exploring a new domain quickly
- the chip is still early and you do not want the full `v2` process overhead
- you want one long architect prompt instead of a prompt stack

Tradeoff:

- faster to start
- less explicit about role separation between architect, operator, implementation, testing, and review

## v2

Use [`docs/master_chip_v2/README.md`](master_chip_v2/README.md) when you want the stricter prompt-stack system.

Use `v2` when:

- the chip is meant to become a durable standard
- you need stronger portability across domains
- you want separate design, implementation, testing, and review passes
- the domain may require new benchmark bridges, watchtower pages, packet families, or explicit contract extensions

Tradeoff:

- slower and heavier
- better for serious standardization and stronger reviewability

## Recommended Decision Rule

- use `v1` for fast exploration, light experiments, and low-ceremony chip planning
- use `v2` for chips you expect to keep, compare, publish, or reuse across domains

If a chip graduates from "quick exploration" into "real standard," rerun it through `v2`.

## Suggested Bakeoff

To compare `v1` and `v2` honestly, build the same chip concept both ways and compare:

- `chips validate` pass/fail
- `autoloop --command research` stability
- packet quality
- watchtower quality
- implementation size and review load
- how much hidden operator knowledge was required

Good candidates:

- a benchmark-heavy domain such as trading
- a research/content domain such as `xcontent`
- a sparse-benchmark domain such as founder coaching or recruiting

That gives you real evidence for where `v1` or `v2` is actually stronger instead of choosing on taste alone.

For the archived rubric and test shape, use [`docs/archive/CHIP_BAKEOFF.md`](archive/CHIP_BAKEOFF.md).
