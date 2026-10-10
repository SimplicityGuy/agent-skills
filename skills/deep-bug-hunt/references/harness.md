# Harness - how to run finders and verifiers

Pick the highest tier this environment supports. The contracts, dedup rules, and operator
gate are identical in every tier; only the plumbing changes.

## Tier A - Claude Code with the Workflow tool

Use the Workflow tool in the background, not ad-hoc parallel Agent calls. **One workflow
per round**, never one per hunt: a background workflow cannot prompt the operator, so the
gate exists only if the workflow returns at each round boundary.

Shape, per lens within a round:

```
pipeline(
  FINDERS,                                   // ~MAX_AGENTS slices covering the whole tree
  finder -> agent(finderPrompt, {schema: FINDER_SCHEMA}),            // session model
  found  -> parallel(found.candidates
              .filter(c => !fingerprints.has(c.fingerprint))          // mechanical dups skip verification
              .map(c => agent(verifyPrompt(c), {model: VERIFIER_MODEL, schema: VERDICT_SCHEMA})))
)
```

- **Pipeline, not barrier.** Each slice's candidates verify the moment that slice
  finishes; nothing waits for the slowest finder.
- **Finder = inherited session model; verifier = `VERIFIER_MODEL`.** That gives the
  different-model check for free and keeps finder cost down. Do not set the finder model
  without a reason.
- **Loop lenses explicitly.** Accumulate a `seen` set (corpus titles and fingerprints
  plus this run's confirmed ones) and feed the current snapshot into every finder and
  verifier prompt so later passes skip earlier hits.
- **No automatic dry-stop.** Run each intended lens explicitly. Declare a lens clean only
  when it completed with zero agent errors and found nothing new.
- **Results.** The workflow returns `{confirmed: [...]}`; dump it to
  `.bughunt/runs/<LABEL>/round-<n>-confirmed.json` and file from there. Per-agent raw
  results are in `journal.jsonl` in the run's transcript directory - read it before
  diagnosing an empty or odd result.
- **Resume is cheap.** Agents with an unchanged `(prompt, opts)` replay from cache, so a
  spend-interrupted run continues by re-invoking with `resumeFromRunId`.
- **Concurrency.** The workflow auto-caps at `min(16, cores-2)`; asking for more just
  queues.

## Tier B - subagents, no Workflow tool

Applies to Claude Code via the Agent/Task tool, Codex with subagents, or any harness that
can spawn parallel workers.

- Dispatch finders in parallel batches of at most `MAX_AGENTS`, one per slice, all in a
  single message so they run concurrently.
- As each finder returns, pre-check fingerprints, then dispatch its verifiers. Do not
  wait for the whole finder batch.
- Require structured output: tell each agent to return only JSON matching the schema in
  `contracts.md`, and reject and re-ask on malformed output.
- Keep the journal yourself: append one line per agent result to
  `.bughunt/runs/<LABEL>/journal.jsonl` (`{role, lens, slice, status, result}`). This is
  what makes a partial round recoverable and an error count checkable.
- An agent that returns nothing, errors, or times out is **incomplete**, not empty.
  Re-dispatch it before closing the lens.

## Tier C - no subagents

Run sequentially in the session: one lens at a time, one slice at a time, writing
candidates to the journal as you go. Shrink the round (fewer slices per pass, or
`CHECKPOINT_EVERY` of 1-2) and tell the operator the hunt will be slower and shallower.

Verification still has to be independent of the finding pass. In order of preference:

1. Shell out to a different model for each candidate, if a CLI for one is installed -
   for example a headless `claude -p` call with a model flag from Codex, or `codex exec`
   from Claude Code. Check the CLI's `--help` for the current flags.
2. A fresh-context pass with the same model, given only the candidate and the verifier
   contract, with none of the finder's reasoning.

## The different-model rule

The verifier must be a different model from the finder wherever the environment allows
it. A different vendor is better still. If the only option is the same model in a fresh
context, do it - but mark those findings "same-model verified" in the provenance footer
and state it plainly at the operator gate, because the confirm rate will run high.

## Escalation for high-stakes classes

For P0 candidates or classes where a false positive is costly, escalate to a **panel**
(3 verifiers; majority refute kills it) or **perspective-diverse** verifiers (one for
reachability, one for existing guards, one for real-world impact). A single different-model
verifier is usually enough.
