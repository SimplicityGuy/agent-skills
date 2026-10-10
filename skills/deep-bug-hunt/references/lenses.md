# Lens catalog

Each lens is its own complete pass over every slice. Adapt to `STACK`: drop lenses with no
surface in the repo (no frontend -> skip lens 6), and add stack-specific ones (IaC or
Terraform, mobile lifecycle, GPU or numerics, FFI/unsafe boundaries). A repo profile may
add concrete emphases under each lens.

1. **Logic & correctness** - wrong results, off-by-one, inverted conditions, missing
   `await` or unhandled promises, mishandled null/None/empty, wrong branch, bad state
   transitions.

2. **Concurrency, races & transactions** - non-atomic read-modify-write, missing row or
   advisory locks (`SELECT ... FOR UPDATE` or equivalent), unawaited or fire-and-forget
   async work, split commits that break atomicity, enqueue-before-commit dual-writes,
   idempotency holes, double-processing, TOCTOU, lost updates from blind UPDATEs,
   job-queue retry and dedup races. *Often the richest lens in service codebases.*

3. **Security & authorization** - authz bypass and IDOR (missing ownership or identity
   checks), SQL / LIKE / template injection, path traversal, SSRF, unsafe subprocess or
   shell, unsafe deserialization, secret leakage into logs or responses, unvalidated
   external input reaching the database, filesystem, or HTTP, network exposure plus weak
   default credentials in deploy config.

4. **Resource & error handling** - leaked connections, HTTP clients, file handles,
   sessions, or subprocesses; missing cleanup on error paths (no `finally`, context
   manager, or defer); bare or broad exception handlers swallowing failures; exceptions
   masked into success-looking returns; error-path recovery that corrupts caller state
   (for example a rollback that invalidates objects the caller still uses); unbounded
   whole-file or whole-corpus reads; pooled connections pinned across slow I/O; retries
   that bypass guards.

5. **Data integrity & persistence** - SQL and query correctness, timezone-naive versus
   -aware datetime mixing, unicode normalization and encoding, column-width and integer
   overflow from unbounded external fields, FK and cascade gaps, ORM-versus-migration
   drift, pagination on unordered queries or without a unique tiebreaker, serialization
   and JSON-column contract mismatches, uniqueness assumptions that do not hold
   (single-row fetches on non-unique keys).

6. **Frontend / UI / template** - partial-update targets that delete the element they
   report into, responses returning stale markup into a redesigned shell, dead DOM ids
   after a UI cutover, swaps or renders duplicating into multiple matches, client-side
   state keys never initialized, stacked or inert modals. *Needs its own pass: these
   hide from backend lenses.*

7. **Config & deploy drift** - deploy and orchestration config versus code expectations
   (auth, read-only mounts versus write paths, ports), container uid and permission
   regressions, env-var defaults, startup ordering, cert and secret bootstrap on a fresh
   host, sidecar and dependency timeouts versus real workloads.

8. **Schema migration** - downgrade and rollback paths, autogenerate drift, revision-id
   collisions, non-atomic DDL, model-versus-migration column mismatches.

9. **Adversarial deep re-read** - the final pass: empty, boundary, and malformed inputs;
   error-path state corruption; cross-module contract violations; dead or unreachable
   safeguards; silent data loss the other lenses skimmed. Aim it at the highest-churn
   files first.

## Ordering

Never-run lenses first (from the hunt history), then historically rich ones for this
repo, then the rest. Lens 9 is always last. Lens short names for labels and
fingerprints: `logic`, `concurrency`, `security`, `resource`, `data-integrity`,
`frontend`, `config`, `migration`, `reread`.
