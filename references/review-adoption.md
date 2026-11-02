# Review, adoption, and checklists

## 18. Change process, review, and definition of done [ALL]

### Before writing

- Understand the user outcome, not just the requested implementation.
- Search for an existing solution and inspect dependency direction.
- List invariant(s), edge cases and failure consequences.
- Prefer a measurable acceptance test.

### During implementation

- Keep changes narrowly scoped and coherent, with tests included.
- Use named decisions, simple branching and bounded side effects.
- Avoid dead code, unused extension points and duplicate sources of truth.
- Preserve backwards compatibility or document deliberate breaks and migration.

### Before merge

- Review correctness and domain rules; auth/tenant boundaries; error/cancellation behavior; concurrency; data migrations; accessibility; performance effects; test coverage; observability; user-facing failures; operational rollback.
- Run tests with actual configured toolchain. Confirm exit codes and capture known limitations.
- Require evidence for new runtime infrastructure or dependencies.
- Ensure docs and examples match code.

## 20. Adoption roadmap and scorecard

### Phase 0 — Inventory, not refactor

- Identify supported language/runtime, app type, entry points, deployments, data stores, dependencies, tests, CI, sensitive operations and owners.
- Read code and test evidence; mark each applicable control with the SKILL.md §4 statuses. Uninspected controls are Unknown.
- Record known incidents, bottlenecks, security obligations and user friction.

### Phase 1 — Establish quality foundations

- Reproducible bootstrap; formatter/linter/type checker; critical tests; basic secure configuration; dependency visibility; change review; explicit error handling.
- Fix correctness/security regressions first; avoid blanket rewrites.

### Phase 2 — Improve maintainability

- Clarify modules and naming; remove accidental duplication; test business invariants; improve contracts and documentation; eliminate unjustified complexity.

### Phase 3 — Harden production behavior

- Add relevant instrumentation, readiness, recovery tests, bounded retries, idempotency, backups and migration safety according to risks of this application.

### Phase 4 — Optimize using evidence

- Profile user and infrastructure bottlenecks; optimize algorithms, SQL and client bundles before selecting caches or distributed components.

### Phase 5 — Reassess periodically

- Track bug escape rate, cycle/feedback time, change failure/recovery, flaky tests, security findings, latency and operating cost. Don't turn metrics into vanity targets.

## 21. Reusable review checklists

### Every pull request

- [ ] Solves a clear requirement with the smallest coherent change.
- [ ] No unnecessary abstractions, dependency additions, dead code or unrelated refactoring.
- [ ] Naming, domain rules, data ownership and side effects are clear.
- [ ] Relevant errors, cancellation, validation and security checks are present.
- [ ] Appropriate tests, formatting, linting, typing and build checks ran and passed—or limitations are explicitly stated.
- [ ] Important documentation, migration, observable behavior and rollback implications are accounted for.

### Public/API or database change

- [ ] Compatibility, auth, authorization, input bounds and error contracts are verified.
- [ ] DB constraints, indexes, isolation, concurrency and migrations are addressed where applicable.
- [ ] Idempotency and ambiguous external outcomes are handled for consequential writes.
- [ ] Tests use actual integration boundaries where needed.

### New infrastructure or design pattern (depth scaled per SKILL.md §2)

- [ ] A real problem is demonstrated with evidence.
- [ ] Existing simpler alternatives have been considered.
- [ ] Benefits exceed added deployment, runtime and maintenance costs.
- [ ] Failure modes, performance, ownership, access control and rollback are documented.
- [ ] A measurable adoption and removal criterion exists.

### Agent-generated changes

- [ ] Existing architecture examined before implementation.
- [ ] No prompt injection or untrusted content promoted to instruction authority.
- [ ] No unapproved destructive action or secret access.
- [ ] Code and tests reviewed for actual behavior, not only plausible output.
- [ ] Final report labels claims Verified, Unverified, Deferred or Unknown (SKILL.md §5).

## Finding template

Use one block per real gap or risk; passing checks get no block.

```md
### <one-line statement of the gap>

Status: Partial | Missing | Unverified | Deferred | Unknown
Severity: Critical | High | Medium | Low
Confidence: High | Medium | Low

Evidence: path/to/file:line; test name or observed behavior
Impact: concrete failure, risk, or maintenance cost
Recommendation: smallest justified change
Verification: acceptance test; failure or edge case; remaining uncertainty
```
