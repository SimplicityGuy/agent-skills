# Finder and verifier contracts

Put the relevant contract into each agent's prompt more or less verbatim, along with the
corpus (`{id, title}`, titles trimmed to ~120 chars) and the fingerprint set.

## Finder contract

**Input:** one lens, an explicit file list (directories recurse), the corpus, the
fingerprint set. Report only bugs rooted in your own scope.

**What counts.** A genuine defect with a concrete failure scenario: wrong output, crash
or 500, data loss, silent data corruption, security hole, resource leak, deadlock or
wedge, or a race.

**What does not.** Style, naming, missing tests, "could be cleaner", speculative "might
be slow", or anything you cannot tie to a reachable failure. Do not report anything
already in the corpus or matching a known fingerprint. Prefer a few high-confidence
findings over many weak ones. **An empty result is a valid, expected answer.**

**Schema** - return `{"candidates": [...]}`, each candidate:

```json
{
  "title": "defect + consequence, precise",
  "file": "path/from/repo/root.py",
  "line": 123,
  "symbol": "enclosing function or class",
  "bug_class": "short-kebab-class, e.g. lost-update",
  "fingerprint": "<lens>:<path>:<symbol>:<bug_class>",
  "severity": "P0|P1|P2|P3",
  "description": "quotes the buggy code and explains the mechanism",
  "failure_scenario": "inputs/state -> bad outcome",
  "fix_hint": "the smallest plausible fix"
}
```

## Verifier contract

**Input:** one candidate, the corpus. A different model from the finder. Your job is to
**refute** the candidate.

- **Default to refuted.** `is_real_bug: true` only if you genuinely could not refute it.
- **Open the actual current file**, plus related models, migrations, and callers.
  Confirm that the cited code exists and says what is claimed; that the failure path is
  **reachable**; that no existing guard, validation, cast, lock, or handler already
  prevents it; and that the behavior is actually wrong *given how the code is called*.
- **Cite exact line contents** as evidence in `reasoning`. No hand-waving.
- **Correct the finding** in `extra_detail`: fix a wrong file or line, add root-cause
  depth, list additional affected sites, and **right-size severity**. Finders routinely
  overstate blast radius - "corrupts stats" when the query uses `COUNT(DISTINCT ...)`.
- **Judge duplication** against the corpus. This is a hint for the hunt lead, not the
  final word.

**Schema:**

```json
{
  "is_real_bug": true,
  "is_duplicate": false,
  "duplicate_of": null,
  "confidence": "high|med|low",
  "severity": "P0|P1|P2|P3",
  "reasoning": "with quoted lines",
  "extra_detail": "corrections, extra sites, root cause"
}
```

## At the filing gate

- Keep only `is_real_bug: true`.
- Drop `confidence: low`.
- Severity comes from the verifier, not the finder.
- A confirmed finding carries forward the finder's description, failure scenario, and
  fix hint plus the verifier's reasoning and extra detail - reuse that text in the issue
  body rather than regenerating it. It saves spend and preserves the evidence.
