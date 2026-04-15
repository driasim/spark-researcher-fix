# Chip Bakeoff

Use this document to compare chip design systems without guessing.

The goal is not to crown a winner from vibes.
The goal is to learn which system works better for which kinds of chip domains.

## Scope

Compare:

- `v1`: [`docs/MASTER_CHIP_ARCHITECT_PROMPT.md`](../MASTER_CHIP_ARCHITECT_PROMPT.md)
- `v2`: [`docs/master_chip_v2/README.md`](../master_chip_v2/README.md)

Shared runtime contract:

- [`docs/CHIPS.md`](../CHIPS.md)

Chooser and framing:

- [`docs/CHIP_SYSTEMS.md`](../CHIP_SYSTEMS.md)

Recommended workspace:

- external repo at `..\spark-chip-bakeoff`

Keep the bakeoff implementation and artifact residue there instead of inside `spark-researcher`.

## Questions To Answer

For each candidate domain:

1. Which system produces a chip that is easier to implement correctly?
2. Which system produces stronger runtime behavior?
3. Which system produces better packets and watchtower surfaces?
4. Which system requires less hidden operator knowledge?
5. Which system is better for this domain category?

## Candidate Domains

Run the bakeoff on at least three domain types:

1. Benchmark-heavy domain
   Suggested: trading
2. Research/content domain
   Suggested: `xcontent`
3. Sparse-benchmark doctrine-heavy domain
   Suggested: founder coaching or recruiting

This matters because one system may be better for strict benchmark domains while another may be better for faster exploration.

## Test Shape

For each domain:

1. Create a `v1` design packet.
2. Create a `v2` design packet.
3. Implement both chips against the same Spark runtime contract.
4. Validate both chips the same way.
5. Run the same bounded evaluation sequence.
6. Score them on the same rubric.

Keep the domain, benchmark assumptions, and operator intent fixed between the two versions.

Do not let one version win just because it got more operator hand-holding.

## Required Checks

Each chip should be checked with:

- `spark-researcher chips validate`
- `spark-researcher collective ready`
- `spark-researcher autoloop --command research`
- packet inspection
- watchtower inspection
- review pass against the current runtime contract

If a domain requires manual setup or external APIs, record that explicitly instead of silently compensating for one system.

## Scorecard

Use a 0-5 score for each category.

### Build Quality

- correctness of scaffold and manifest
- clarity of repo shape
- amount of implementation churn required after first pass
- testability

### Runtime Quality

- `chips validate` pass/fail
- `autoloop` stability
- parseable metrics and hook outputs
- clean failure behavior

### Intelligence Quality

- quality of suggestions
- quality of packets
- honesty about evidence and boundaries
- promotion safety

### Operator Quality

- clarity of generated README and docs
- review burden
- amount of hidden operator knowledge needed
- ease of explaining the chip to another agent/operator

### Watchtower Quality

- usefulness of Obsidian pages
- signal-to-noise ratio
- whether grounded doctrine and exploratory frontier stay clearly separated

## Required Artifacts

For each bakeoff pair, keep:

- the design prompts or prompt outputs
- implementation diff or repo snapshot
- validation output
- one `autoloop` run artifact set
- packet samples
- watchtower page samples
- reviewer verdict

If possible, keep these under a dedicated external experiment repo rather than bloating the kernel repo.

## Expected Outcome Format

At the end of each bakeoff, write:

- which system won for this domain
- why it won
- where it lost
- whether the loser should still be preferred for speed or lower ceremony
- what should become durable cross-domain guidance in Spark docs

## Decision Rule

Do not pick one universal winner unless the evidence actually supports that.

A good outcome might be:

- `v1` is better for fast exploratory chips
- `v2` is better for serious reusable chips

That is still a useful result.

## Non-Goals

- do not rewrite the Spark runtime contract during the bakeoff
- do not archive docs mid-bakeoff
- do not change evaluation criteria between `v1` and `v2`
- do not let one chip use extra undocumented operator intervention
