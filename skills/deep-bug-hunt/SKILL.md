---
name: deep-bug-hunt
description: Run a deep, multi-agent bug-hunt expedition over a whole codebase - one finder pass per bug-class lens, a different-model adversarial verifier that tries to refute every candidate, fingerprint plus judgment dedup against the issue tracker, and filing of only verified, non-duplicate defects, in operator-gated rounds. Use when the user asks for a bug hunt, bug sweep, "find bugs across the repo", a deep defect audit, or to resume or continue a previous hunt. Not for reviewing a single diff or PR, and not for fixing bugs.
---

# Deep Bug-Hunt Expedition

You are the hunt lead. You orchestrate finders and verifiers, own dedup, file the
survivors, and report to the operator at every round boundary. You do not fix anything:
the output of a hunt is filed issues and a run log, never code changes.

The shape of a hunt:

```
preflight -> [ round: N lens passes -> verify -> dedup -> file -> metrics -> ASK OPERATOR ] -> wrap-up
```

Reference files (read when you reach that step, not up front):

| File | Read it when |
|---|---|
| `references/harness.md` | Before launching the first round - how to run finders/verifiers in this agent environment |
| `references/lenses.md` | When writing finder prompts - the lens catalog |
| `references/contracts.md` | When writing finder and verifier prompts - contracts and schemas |
| `references/dedup.md` | Before filing anything - fingerprints and judgment dedup |
| `references/tracker.md` | Before the first tracker command - bd, GitHub Issues, and file-based trackers |
| `profiles/TEMPLATE.md` | At wrap-up, when saving a profile for a repo that has none |

## 1. Parameters

Resolve these in preflight. Sources, in priority order: what the operator said when
invoking the skill, then the repo profile, then the defaults.

| Parameter | Meaning | Default |
|---|---|---|
| `STACK` | Languages/frameworks; steers lens emphasis | Detect from the repo |
| `TRACKER` | Where bugs are listed and filed | Detect: `.beads/` -> `bd`; GitHub remote -> `gh`; else a JSONL file |
| `VERIFIER_MODEL` | A model **different from the finder model** | `opus` in Claude Code; see `references/harness.md` elsewhere |
| `LABEL` | Label for this hunt's filings; one per hunt, never reused | `bughunt-<YYYY-MM-DD>` |
| `MAX_AGENTS` | Concurrency cap | 16 |
| `MAX_PASSES` | Hard ceiling on lens passes | 10 |
| `CHECKPOINT_EVERY` | Lens passes per round | 3 |
| Scope | Optional narrowing | Whole tree, all lenses |

Scope add-ons the operator may give: only certain lenses; only files changed since a
ref; skip anything already carrying a `bughunt-*` label.

**Repo profile.** Nothing in this skill is specific to any repo; everything
repo-specific lives in `.bughunt/profile.md` inside the repo itself. A profile supplies parameters, a
slicing plan, lens emphases, tracker quirks, and the hunt history. If none exists,
derive what you need from the repo and offer at wrap-up to save one from
`profiles/TEMPLATE.md`.

**Severity mapping** (keep it stable across hunts or the trend metrics are noise):
P0 crash, data loss, or authz bypass · P1 wrong behavior in normal use · P2 edge case ·
P3 latent.

## 2. Preflight

1. Confirm you are in the right repo and the right tracker database (see
   `references/tracker.md`). A batch filed into the wrong database is tedious to unwind.
2. Load the corpus: every open bug as `{id, title}`, plus every `hunt_fingerprint` ever
   filed across all hunts. This is the dedup memory.
3. Read the hunt history (`.bughunt/HUNTS.md` or the profile footer). Un-run lenses and
   un-sliced areas from earlier hunts are un-swept ground and go first.
4. Build the slicing plan: about `MAX_AGENTS` balanced groups of files by area, with an
   explicit file list per slice. Every source file belongs to exactly one slice.
5. Choose the lens order (`references/lenses.md`): drop lenses with no surface in this
   repo, add stack-specific ones, put never-run lenses first, then historically rich ones.
6. Create `.bughunt/runs/<LABEL>/` and write `plan.md` (parameters, slices, lens order).
7. Tell the operator the plan in a few lines, then start. Only wait for an answer if a
   parameter is genuinely ambiguous (for example, no tracker can be detected).

## 3. The round loop

A round is `CHECKPOINT_EVERY` lens passes. **Each round is its own unit of background
work that returns to you** - never one monolithic run spanning the whole hunt. Background
work cannot ask the operator anything, so the gate in step 7 only exists if the work
comes back at each round boundary. If you find yourself wanting to ask mid-round, the
round was scoped too large.

For each round:

1. **Run the lens passes** (`references/harness.md`). Each lens is a complete pass over
   every slice. Each finder gets: its lens, its file list, the finder contract, the
   corpus titles, and the fingerprint set. A lens finding nothing does not end the hunt;
   the next lens may be rich.
2. **Pre-check fingerprints.** A candidate whose fingerprint exactly matches a filed one
   is a mechanical duplicate: log it and skip the verifier. This is the cheapest saving
   in the harness.
3. **Verify.** Every remaining candidate goes to one `VERIFIER_MODEL` verifier whose job
   is to refute it (`references/contracts.md`). Verify as each finder lands rather than
   waiting for the slowest one.
4. **Check the run was real.** If any agent errored or aborted, the round is incomplete.
   Aborted agents return nothing, which looks exactly like "no bugs found". Resume the
   un-run work and tell the operator; never report that result as convergence.
5. **Persist** the confirmed set to `.bughunt/runs/<LABEL>/round-<n>-confirmed.json`,
   and record which slices and lenses actually completed in `coverage.md`.
6. **Dedup, then file** (`references/dedup.md`, `references/tracker.md`). Drop
   `confidence: low`. Dedup the confirmed set by hand against the corpus and against
   itself. Dry-run the filing batch, file, run the near-duplicate net, then export/sync
   the tracker so the next round's corpus load sees this round's filings.
7. **Compute metrics and stop at the operator gate** (section 5).

Ambiguous candidates - threat-model-dependent, needing a specific repro, or contradicting
a prior verdict - are filed anyway, with a **triage note** spelling out what to confirm.

## 4. Dedup is yours

The verifier's `is_duplicate` flag under-flags badly; a large share of "confirmed,
non-duplicate" findings typically turn out to be restatements of existing issues. Treat the flag
as a hint. Before filing, re-check every confirmed finding yourself, and **read the body
of any issue a finding might duplicate** - consolidated issues cover more than their
titles say, and sometimes less than a summary note claims.

File one issue per distinct defect. Merge findings that share one root cause and one
fix. Keep same-class, different-site findings separate and cross-reference them. Never
silently drop a real finding: a true duplicate is still recorded against its canonical
issue, so the next hunt does not pay to re-discover and re-adjudicate it. Full rules in
`references/dedup.md`.

## 5. Metrics, stop criteria, and the operator gate

Compute per pass, report per round, always against all prior rounds:

| Metric | Definition | Reading |
|---|---|---|
| Confirm rate | confirmed / candidates | Finder precision. Collapsing means finders are scraping the barrel. |
| Novelty rate | filed-after-dedup / confirmed | **The convergence metric.** Duplicate rate is 1 minus this. |
| Severity mix | P0-P1 share of filed | Near zero while volume holds means real but low-value yield. |
| Per-lens yield | filed, by lens | A still-rich lens justifies another round. |
| Cost per filed bug | round spend / filed | What the operator needs to judge "worth another round?" |

Convergence is novelty and severity together. A round that files 20 P3s after a round
that filed 4 P0s is a decline, whatever the count says.

**Hard stops** - report and stop without asking:

- `MAX_PASSES` reached.
- Every lens in the catalog completed cleanly, with zero new filings in the most recent
  full lens cycle.
- Two consecutive rounds with novelty rate below 0.15 and zero P0/P1.

A round with a non-zero agent error count is never a stop; see step 4 above.

**The operator gate** - at every round boundary, stop and ask the operator
directly (use the environment's question tool if it has one, such as `AskUserQuestion`;
otherwise ask in plain text and end your turn). Present:

1. The metrics table, this round against all prior rounds, with a tally by lens and severity.
2. Lenses run, lenses not yet run, and areas of the tree not yet sliced.
3. Approximate spend this round and cost per filed bug.
4. Your recommendation, with a reason. "Concurrency filed 6 including 2 P0s and is not
   exhausted; recommend 2 more rounds" beats a neutral menu.

Offer concrete options: continue N more rounds · continue but narrow to the
still-productive lenses · switch to un-run lenses or areas only · stop and wrap up.

Do not auto-continue past a round boundary, and do not stop early on your own outside the
hard stops. While new bugs are still landing, say "still productive" and let the operator
decide; never imply convergence.

**Flat yield is a finding in its own right.** If three rounds in a row hold steady on
both novelty and severity, say so plainly: the repo has a systemic defect density, and a
targeted remediation epic on the dominant bug class is probably a better next move than
another round of the same sweep.

## 6. Wrap-up

- Final tally by lens and severity, and the per-round metrics.
- Append an entry to `.bughunt/HUNTS.md`: date, `LABEL`, rounds run and the operator's
  decision at each gate, per-round metrics (candidates -> confirmed -> filed, novelty
  rate, severity mix), corpus size before and after, and explicitly un-run ground.
- Record any new tracker quirks or recurring bug classes in the repo profile.
- If the hunt filed enough to be a work item rather than a list, suggest grouping the
  batch under an epic so remediation can be dispatched as a unit.
- Final tracker export/sync. An unsynced batch is invisible to the next hunt's corpus
  load, which guarantees duplicates next time.

## 7. Things that will mislead you

- **Spend limits and API failures truncate silently** and manufacture a false dry
  signal. Check the error count on every completed round before believing a zero.
- **A skipped lens is un-swept ground, not clean ground.** "We swept everything" has to
  be provable from `coverage.md`.
- **Finders overstate blast radius.** Severity comes from the verifier.
- **Titles lie by omission**, in both directions. Read issue bodies before deciding.
- **Volume is not progress.** Read novelty and severity together.
- **Tracker CLI flags drift between versions.** Check `--help` and dry-run before the
  first batch; a malformed loop that files 40 half-formed issues is expensive to unwind.
