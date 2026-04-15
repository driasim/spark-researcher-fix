# Chip Authoring

This guide is for building a Spark domain chip with an LLM while keeping the result modular and reviewable.

## What A Domain Chip Can Be

A chip does not have to be "domain knowledge only."

A good chip can govern:

- research loops for a topic or niche
- prompt or evaluator optimization
- content systems
- trading or strategy analysis
- startup or operator workflows
- coding or review workflows
- browser or API task loops
- internal tools or plugins that should improve over time

The right question is:

- what task should improve
- what outcome should count as better
- what mutations should the loop be allowed to try

If you can answer those cleanly, a chip is probably a good fit.

## When To Make A Chip

Make a chip when the kernel should stay generic but the task needs custom logic for:

- evaluation
- suggestion generation
- memory packet promotion
- watchtower rendering

Do not put that logic into the Spark kernel if it is really specific to one task family.

## A Good Chip Brief

Before asking an LLM to build the chip, write down:

- the task the chip is improving
- the command or hook that should run
- the primary metric
- whether lower or higher is better
- the main mutation fields
- what a strong result should promote into memory
- what an operator should see in Obsidian

Minimal example:

- task: improve outbound founder-research packets
- command: `research`
- metric: `packet_quality_score`
- goal: `maximize`
- mutation fields: `audience_segment`, `packet_style`, `source_mix`, `claim_density`
- memory tiers: `grounded_doctrine`, `grounded_boundary`, `benchmark_evidence`, `exploratory_frontier`

## What To Tell Your LLM

When working with an LLM, keep the instructions concrete.

Good guidance looks like:

- build this as a standalone `domain-chip-*` repo outside `spark-researcher`
- keep Spark kernel changes at zero unless a true runtime gap is discovered
- implement the chip through the standard hooks: `evaluate`, `suggest`, `packets`, `watchtower`
- make the evaluator honest before making it clever
- keep mutation fields explicit and reviewable
- add tests for evaluator behavior and watchtower truthfulness
- prefer small packet families over verbose output

Useful prompt shape:

```text
Create a Spark domain chip for <task>.

The chip should improve <specific task>.
Primary metric: <metric_name>.
Goal: <maximize|minimize>.
Allowed mutations: <field list>.

Implement:
- evaluate
- suggest
- packets
- watchtower

Keep the Spark kernel generic.
Keep the chip as an external repo.
Add tests for the evaluator, packets, and watchtower.
Use grounded_doctrine, grounded_boundary, benchmark_evidence, and exploratory_frontier as the main packet kinds unless there is a strong reason not to.
```

## What Kinds Of Chips To Consider

High-signal chip ideas:

- a browser-task chip that grades task completion quality, retries, and operator burden
- a coding-review chip that scores bug-finding accuracy or regression coverage
- a support chip that improves reply quality against resolution and customer-friction metrics
- a content chip that improves post quality against meaningful engagement, not vanity reach
- a startup chip that improves research packets, prioritization, or GTM experiments
- a tool-plugin chip that improves how a tool is used over repeated runs

The pattern is the same:

- task surface
- metric surface
- mutation surface
- memory surface

## Recommended Build Flow

1. Create the scaffold.

```powershell
spark-researcher chips init --domain foo --metric-name foo_score --goal maximize
```

2. Ask your LLM to turn the scaffold into a real chip by implementing:

- `evaluate`
- `suggest`
- `packets`
- `watchtower`

3. Keep the repo modular:

- chip-specific docs stay in the chip repo
- chip-specific source stays in the chip repo
- only kernel-wide runtime changes belong in `spark-researcher`

4. Validate the chip.

```powershell
spark-researcher chips validate
spark-researcher collective ready
```

5. Run bounded autoloops.

```powershell
spark-researcher autoloop --command research --rounds 4 --suggest-limit 4
spark-researcher memory sync
spark-researcher obsidian build
spark-researcher summary
```

6. Review what happened:

- did the metric move honestly
- are suggestions bounded and defensible
- are promoted packets actually useful
- does watchtower reflect truth instead of a cleaned-up story

## How To Guide Your LLM During Iteration

The LLM usually needs stronger guardrails than "make this better."

Useful iteration prompts:

- make `suggest` more conservative and evidence-led
- separate grounded doctrine from exploratory frontier
- add a contradiction probe for the strongest promoted pattern
- make the watchtower pages more reviewable, not more verbose
- add tests for the highest-risk evaluator branches
- keep the mutation grammar fixed and explicit

Bad iteration prompts:

- make it smarter
- make it more agentic
- add more AI

Those usually create drift instead of quality.

## How To Think About Plugins And Tools

Spark can also sit above tools and plugins.

If a tool or plugin can be run, judged, and improved through bounded mutations, it can usually be wrapped in a Spark chip.

Examples:

- a browser tool plugin that runs a workflow and gets scored on completion quality
- a codegen plugin that gets scored on test pass rate or review findings
- a data-enrichment tool that gets scored on precision and downstream usefulness

In those cases, the chip does not just gather knowledge.
It teaches Spark how to improve task execution.

## Rule Of Thumb

If your LLM can clearly explain:

- what changed
- why that change should improve the metric
- what boundary keeps it honest

then you are probably building a usable Spark chip.

If it cannot explain those three things, tighten the brief before you run more loops.
