# Dedup

The single most important step, and the hunt lead's own job. The verifier's
`is_duplicate` under-flags: a large share of "confirmed, non-duplicate" findings turn out
to be restatements of existing issues.

## Two memories

- **Within a round** (candidate versus candidate, dozens of items, all in hand): dedup
  in the session with fingerprints, before any filing. Tracker round-trips here are slow
  and buy nothing.
- **Across rounds and hunts** (candidate versus everything ever filed): the tracker is
  the only thing that remembers. This is what stops hunt #4 re-filing hunt #2's findings.

## Fingerprints

Every finding gets a stable key:

```
<lens>:<normalized-path>:<symbol-or-nearest-enclosing-function>:<bug-class>
e.g. concurrency:app/svc/order.py:reserve_stock:lost-update
```

Deliberately **not** line numbers (they drift) and **not** titles (models rephrase
freely). Store it on the issue at filing time so it is queryable later (see
`tracker.md`). Load every fingerprint ever filed at the start of each round.

An exact fingerprint hit is a mechanical duplicate: drop it at the finder stage, with a
log line, before spending a verifier on it. Fingerprints catch the obvious repeats, not
the rephrased ones - everything else still goes through judgment dedup. Note the lens is
part of the key, so the same defect found under a different lens will not hit; judgment
dedup catches that.

## Judgment dedup of the confirmed set (before filing)

1. Re-check every confirmed finding against (a) the corpus and (b) the other confirmed
   findings this round.
2. **Read the body of any issue a finding might duplicate** before deciding. Titles lie
   by omission: a consolidated issue (say, a repo-wide input-validation sweep) can cover
   sites its title never names, and can also cover *less* than a checkpoint note claims.
3. Apply the heuristics:
   - **Same function, different defect -> distinct** (an injection bug and a TOCTOU race
     in the same function).
   - **Same column or field, different write path or endpoint -> distinct** (two
     independent code paths hitting the same constraint).
   - **Same root cause and same fix, two layers -> merge** (an endpoint and the service
     function it calls, when one guard fixes both).
   - **Same bug class, different site -> separate, cross-referenced** (the same
     error-handling flaw on two pages: two issues, each naming the other).
   - **Path/URL parameter versus body field -> distinct** (body-schema validation cannot
     cap a URL path segment).
4. Cross-reference with a real link or dependency edge where the tracker has one, not
   only prose, so the relationship is visible from either end.

## Never silently drop

A genuine finding near an existing one, if distinct, is filed with a note pointing at the
neighbor. A true duplicate is still recorded, one of two ways:

- **Merge:** append the new site and evidence to the canonical issue and link them.
- **File and mark:** file it, then mark it a duplicate of the canonical issue (which
  closes it with a pointer).

The second costs one extra issue and buys a permanent, fingerprinted record that this
finding was found and adjudicated. Without it, every future hunt re-discovers,
re-verifies, and re-adjudicates the same thing - the largest source of wasted spend
across repeated hunts. Prefer file-and-mark when the fingerprint differs from the
canonical issue's; prefer merge when it adds a new site to the same defect.

## After filing: the near-duplicate net

If the tracker has a similarity search (for example `bd find-duplicates`), run it over
the fresh filings and adjudicate each pair. Treat it as a net, not a decision-maker:
mechanical similarity over titles is exactly the thing that under-flags.

## Count it

Track per round: candidates, mechanical-duplicate drops, confirmed, judged duplicates,
filed. Novelty rate (`filed / confirmed`) is the hunt's convergence metric and is only
computable if duplicates are counted rather than quietly discarded.
