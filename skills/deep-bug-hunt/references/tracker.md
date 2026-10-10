# Tracker mechanics

Whatever the tracker, the filing rules are the same:

- Script the batch from `round-<n>-confirmed.json`; capture the returned ids into
  `round-<n>-filed.json`.
- **Dry-run first.** Check the CLI's `--help` for the current flag names before the
  first batch - they drift between versions.
- Every issue carries: type bug; priority from the **verifier's** severity; labels
  `LABEL`, `lens-<lens>`, `pass-<n>`, `sev-p<0-3>`; the fingerprint; a provenance footer.
- Flat, prefixed labels only (`lens-concurrency`), so pattern queries work. A typo'd
  label is an invisible issue; list the labels after a batch and check.
- One `LABEL` per hunt, never reused. Cross-hunt queries go through the fingerprint.
- Export/sync after every batch.

## Issue body template

```
<finder description, quoting the buggy code>

## Failure scenario
<inputs/state -> bad outcome>

## Fix hint
<...>

## Verification
<verifier reasoning with quoted lines; extra_detail: corrections, other sites>

## Triage note            (only for judgment calls)
<threat-model dependence / repro needed / contradicts prior verdict / merge-split relations>

---
Hunt <LABEL> · lens <lens> · pass <n> · slice <slice> · <file>:<line>
Adversarially verified (<VERIFIER_MODEL>) · confidence <high|med>
Fingerprint: <fingerprint>
```

## bd (beads)

Preflight: `bd status` to confirm the repo and database - if bd is reached through a
wrapper or multi-repo router, make sure it resolves to this repo's database. Set `CI=1`
to keep bd non-interactive.

Corpus load:

```
bd list --type bug --status open --json              # open-bug corpus
bd list --has-metadata-key hunt_fingerprint --json   # every fingerprint, all hunts
bd list --label <LABEL> --json                       # this hunt's filings
bd show <id> --json                                  # read a body before judging a dup
```

File:

```
bd create "<title>" --type bug -p <0-3> \
   --labels <LABEL>,lens-<lens>,pass-<n>,sev-p<n> \
   --metadata '{"hunt_fingerprint":"...","hunt_id":"<LABEL>","hunt_lens":"<lens>","hunt_pass":<n>,"finder_slice":"<slice>"}' \
   --body-file -            # body on stdin; add --dry-run for the rehearsal
```

Dedup and links:

```
bd duplicate <new> --of <canonical>            # file-and-mark
bd note <canonical> "<new site + evidence>"    # merge
bd dep link <a> <b> --type related             # cross-reference
bd find-duplicates --threshold 0.4 --json      # near-duplicate net, after a batch
bd label list-all                              # check for typo'd labels
```

Sync: `bd export -o .beads/issues.jsonl`, then `bd dolt push` if the repo uses a dolt
remote. Large batches can be grouped: `bd create --type epic`, then `--parent`.

Known quirks (verify against the installed version):

- There is no `bd sync`; use `bd export`.
- `bd show` and `bd list --json` return a JSON **array** - index `[0]` for one issue.
- `bd comment <id> "text"` has no `add` subverb.
- Older versions take the body with `--stdin --silent` instead of `--body-file -`, and
  may lack `--metadata`, `duplicate`, or `find-duplicates`. If metadata is unavailable,
  fall back to the `Fingerprint:` footer line and search bodies for it.
- Shell aliases can shadow tracker wrappers; call the `bd` binary directly.
- `--external-ref` keeps a GitHub/Jira mirror idempotent on re-runs.

## GitHub Issues (gh)

Preflight: `gh repo view --json nameWithOwner` to confirm the repo.

```
gh issue list --state open --label bug --limit 1000 --json number,title,labels
gh issue list --state all --search '"Fingerprint:" in:body' --limit 1000 --json number,body
gh issue view <n> --json title,body
gh issue create --title "<title>" --body-file - \
   --label bug,<LABEL>,lens-<lens>,pass-<n>,sev-p<n>
```

- Labels must exist first: `gh label create <name> --force`.
- There is no metadata field: the `Fingerprint:` footer line is the index. Parse it out
  of the bodies at corpus load.
- No dry-run flag: rehearse by printing the commands and writing bodies to
  `.bughunt/runs/<LABEL>/bodies/` for a skim, then file.
- Duplicate: comment `Duplicate of #<canonical>` and close as not planned (or the
  duplicate close reason, if this `gh` version has one). Cross-reference by mentioning
  `#<n>` in both bodies.
- No sync step.

## File-based fallback

No tracker: append one JSON object per finding to `.bughunt/issues.jsonl`
(`id, title, status, priority, labels, fingerprint, duplicate_of, related, body`), with
ids `BH-<n>`. Corpus load is reading that file. Tell the operator at the first gate that
findings are landing in a file, not a tracker.

## Other trackers

Map the same fields: type, priority, labels, fingerprint (a custom field if there is
one, otherwise the footer line), duplicate link, related link, export. Record the
working commands in the repo profile.
