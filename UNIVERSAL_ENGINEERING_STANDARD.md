# Universal Software Engineering Standard

**Edition:** 2026-11-01  
**Scope:** Web, mobile, desktop, API, backend, CLI, data, ML, and AI applications  
**Purpose:** Produce software that is correct, simple, secure, understandable, maintainable, observable, and economical to change.

> **North star:** Choose the least-complex design that reliably meets verified requirements and preserves important invariants. Add complexity only to resolve a real constraint. This document is a set of decision rules, not an instruction to install every technology or apply every pattern.

## Contents

1. Applicability, priority, and evidence
2. Foundational principles
3. SOLID without overengineering
4. Readable code and API design
5. Modules, dependencies, and architecture
6. Choosing design patterns
7. Domain, state, data, and persistence
8. Concurrency and asynchronous processing
9. Resilience and distributed systems
10. Security, privacy, and supply chain
11. Testing and verification
12. Performance and scalability
13. User experience and accessibility
14. Observability and operations
15. Build, CI, delivery, and dependency management
16. Documentation and architectural decisions
17. AI/ML and coding-agent safeguards
18. Change process, review, and definition of done
19. Anti-patterns and their replacements
20. Adoption roadmap and scorecard
21. Reusable review checklists
22. Research sources

---

## 1. Applicability, priority, and evidence

A universal standard must not turn a static site into a distributed system.

### Applicability labels

- **[ALL]** All repositories, including scripts and libraries.
- **[SERVICE]** Any request-serving, networked, or background-running application.
- **[DATA]** Systems that persist important state, process payments, or perform concurrent writes.
- **[UI]** User-facing web, mobile, and desktop applications.
- **[AI]** Model-assisted, data-science, or autonomous-agent systems.
- **[AT SCALE]** Only when measured workload, availability, or organizational requirements justify it.

### Priority rules

- **P0 / required:** Correctness, declared dependencies, formatting and linting, secure defaults, appropriately scoped tests, reproducible builds, error handling, access control where applicable, and safe production operation.
- **P1 / recommended:** Module boundaries, structured diagnostics, automated contract checks, performance budgets, change review, documented runbooks, and integration tests proportionate to risk.
- **P2 / conditional:** Caches, queues, complicated workflow engines, circuit breakers, read replicas, service decomposition, multiple storage engines, and complex policy engines.
- **P3 / evidence-gated:** Sharding, event sourcing, microservices, distributed transactions, speculative plugin systems, universal generic repositories, and custom infrastructure platforms.

**Never mark an item “missing” just because a repository uses a different—but adequate—implementation.** Audit implementation and behavior, not framework or directory naming. For each proposed change document: current evidence, actual failure or cost, simplest option, expected result, verification, and rollback.

### Decision procedure

1. **Identify the requirement:** Is it demanded by a user, a domain invariant, a security obligation, a concrete incident, or a measured bottleneck?
2. **Find the simplest existing mechanism:** Can current code or infrastructure address it?
3. **Estimate cost:** Extra branches, abstractions, processes, dependencies, failure states, runtime services, and ongoing operations all count.
4. **Choose the smallest safe change:** Preserve behavior and existing contracts unless the task deliberately changes them.
5. **Verify:** Test success, failure, cancellation, concurrency, and authorization as applicable.
6. **Measure:** Did it improve correctness, latency, maintenance, user value, or reliability?
7. **Defer deliberately:** Record a trigger or objective criterion for reconsideration, not a wish list.

## 2. Foundational principles

### KISS — Keep It Simple

- Prefer direct, readable control flow over cleverness or indirection.
- Avoid configuration switches without an existing user or environment requiring them.
- Prefer standard libraries and maintained dependencies to custom frameworks.
- Favor small modules with a clear purpose, not artificially tiny functions or files.
- Simplicity includes operational cost: three processes may be more complex than one larger program.

**Counterexample:** A 20-line straightforward function can be easier to maintain than five one-line functions linked through interfaces.

### YAGNI — You Aren't Gonna Need It

- Do not build for hypothetical users, providers, regions, databases, or scale.
- Keep extension points only where concrete multiple implementations exist or an explicit near-term requirement demands them.
- Do not confuse **necessary safety engineering** (validation, migration safety, auth, backups) with speculative future features.
- Avoid generalized engines for problems that are currently solved by ordinary code.

**Trigger to generalize:** Real use cases differ and the invariant/common abstraction is understood.

### DRY — Don't Repeat Yourself

- Remove duplicated **business knowledge**: pricing rules, eligibility policy, schema contracts, permission decisions, and validation invariants.
- Similar syntax is not automatically duplicated knowledge. Two intentionally independent features may reasonably use similar code.
- Avoid sharing an abstraction that forces unrelated consumers to change together.
- Prefer code generation, a single source of truth, or a focused function for truly shared definitions.

**Example:** Repeating a tax-rate rule in a browser and payment service is a correctness risk. Two three-line UI components with similar rendering may remain independent.

### AHA / Rule of Three — Avoid Hasty Abstractions

- First implementation: solve the concrete case cleanly.
- Second: observe what truly repeats and what varies.
- Third: consider extracting a stable abstraction, **not an automatic requirement**.
- Extract earlier when duplication is a security/correctness risk; later when the domain is unsettled.

### Cohesion, Coupling, Separation of Concerns

- Keep related state and behavior together.
- Hide volatile implementation choices behind meaningful boundaries.
- Limit cross-module knowledge and avoid circular dependencies.
- Group by business capability when this improves navigation and ownership; do not reflexively require a framework-wide layered layout.

### Other useful rules

- **Explicitness:** Make important assumptions, error paths, and dependencies visible.
- **Least astonishment:** Naming and API behavior should match the natural interpretation.
- **Encapsulation:** Expose stable behavior, not writable internal state.
- **Composition over inheritance:** Prefer small collaborators, functions, and dependency injection rather than complex hierarchies.
- **Functional core, imperative shell:** Separate deterministic calculations from I/O, time, and randomness when doing so improves testing and clarity.
- **Tell, don't ask:** Prefer operations that preserve an entity's own invariants to external code reaching into its state.
- **Law of Demeter:** Do not casually chain through distant implementation details; avoid rigidly adding forwarding methods for every access.
- **Boy Scout Rule:** Improve nearby code when directly relevant; avoid stealth rewrites.
- **Clarity over LOC count:** Shorter code is not necessarily simpler code.

### Explicit conflict resolution

1. **Correctness and safety outrank DRY and conciseness.**
2. **Observed requirements outrank speculative extensibility.**
3. **Readable local duplication can beat a wrong global abstraction.**
4. **A simple concrete implementation can beat unnecessary dependency inversion.**
5. **Targeted optimization can beat elegant generality when measurement proves it necessary.**
6. **Stable domain constraints beat convenience in UI, ORM, and transport layers.**

## 3. SOLID without overengineering

- **S — Single Responsibility:** One cohesive reason to change. Not “one statement per function.”
- **O — Open/Closed:** Design stable extension seams where variation is real. Do not forbid editing existing code.
- **L — Liskov Substitution:** A substitute honors caller-visible behavior: preconditions, outputs, errors, timing and important invariants.
- **I — Interface Segregation:** Give consumers the narrow methods they need; avoid giant service contracts.
- **D — Dependency Inversion:** Important business logic should not be coupled to vendor/framework details; introduce ports at useful boundaries.

**Default:** Start with concrete types. Introduce small interfaces when tests, multiple implementations, or architectural isolation actually benefit. Place interfaces near their consumer where idiomatic. Don't manufacture repositories, factories, builders, or dependency injection containers for every class or SQL query.

## 4. Readable code and API design [ALL]

### Naming and structure

- Names communicate meaning, domain and units. Prefer `timeoutMilliseconds`, `orderTotal`, `paidAt` over `t`, `data`, `value`.
- Use consistent terminology across UI, API, database, events, and docs. Avoid synonyms for the same concept.
- Keep public APIs small; mark internals private by default.
- Prefer early returns for guard conditions and readable straight-line logic.
- Limit nesting by extracting meaningful operations, not arbitrary lines.
- Keep modules focused; avoid catch-all `utils`, `helpers`, `common`, and `manager` files that accumulate unrelated responsibilities.
- Delete dead paths, unused flags, stale TODOs, commented-out code, and obsolete compatibility shims when safe.
- Comments explain **why**, contracts, invariants, tradeoffs, and non-obvious algorithms. Do not narrate obvious statements.
- Prefer tooling-enforced style over subjective review debate. Format and lint in CI.

### Functions and types

- Make inputs, outputs, side effects, and failure modes clear.
- Prefer typed domain values for money, identifiers, timestamps, permissions, and state transitions where they prevent real bugs.
- Avoid primitives that mix currencies, units, tenant IDs, or time zones.
- Prefer immutable data when mutation adds no benefit; otherwise make mutation ownership explicit.
- Prefer exhaustive handling of enums/state variants when language tooling supports it.
- Validate untrusted input at boundaries and domain invariants in the domain.
- Avoid `any`, unchecked casts, reflection, or dynamic dispatch when they bypass important guarantees; make justified exceptions local.
- Avoid magic numbers/strings when domain semantics are hidden, but don't create constants for universally obvious values.
- Avoid boolean-parameter traps (`save(true,false,true)`); use named options or explicit operations when ambiguous.
- Define clear error categories and retain causes; never silently swallow failures.
- Distinguish expected business rejections from system faults; do not expose internal stack traces to clients.
- Prefer stable, explicit public contracts and version or migrate breaking changes intentionally.

### Side effects and lifecycle

- Pass cancellation, timeouts, and deadlines into I/O operations when supported.
- Close resources, cancel spawned work, and free handles deterministically.
- Make ownership of threads, connections, caches, temporary files, and locks explicit.
- Do not initiate hidden network or database activity in pure-looking accessors or constructors.
- Keep clock and randomness dependencies controllable where deterministic testing is important.

## 5. Modules, dependencies, and architecture [ALL]

- Start with a single deployable application or the existing architecture unless actual requirements justify distribution.
- Group by feature/domain capability, with separation of domain, use cases, and external adapters where helpful.
- Domain/business rules must not depend on HTTP headers, UI components, cloud SDK types, or concrete database clients.
- Use explicit contracts for real boundaries: payment provider, notification transport, persistence of important aggregates, external APIs.
- Use anti-corruption adapters to translate external models into internal vocabulary.
- Avoid framework leakage through the domain.
- Keep dependency direction intentional and forbid dependency cycles.
- Use architecture fitness checks when practical (import rules, dependency graph checks, schema compatibility tests).
- A feature's code should be discoverable without opening dozens of unrelated directories.
- Treat shared libraries as products with owners, stable contracts and reasoned consumers—not dumping grounds.

### Architecture selection

| Condition | Default |
| --- | --- |
| Small program, CLI, prototype | Simple modules and direct functions |
| Growing application with business logic | Feature modules, clear boundaries, single deployable |
| External integrations | Ports/adapters at real vendor boundaries |
| Complex domain invariants | State machines, value objects, focused DDD |
| Distinct read/write shapes | Separate command/query handlers; full CQRS only if justified |
| Independent scaling/deployment needs, stable ownership | Evaluate services and operational tradeoffs |
| Historical replay is an explicit requirement | Evaluate event sourcing and its migration cost |

**Architecture review question:** “Which concrete change, failure, or dependency does this boundary make easier?” If there is no credible answer, simplify.

## 6. Choosing design patterns [ALL]

| Problem | Prefer | Watch out for |
| --- | --- | --- |
| Third-party interface mismatches | Adapter | Leaking provider models into domain |
| Cross-cutting logging/metrics | Decorator/middleware | Deep opaque wrapper stacks |
| Complex subsystem usage | Facade | God facade doing all business logic |
| Multiple real algorithms | Strategy/functions | Strategy interface for one implementation |
| Valid lifecycle transitions | Explicit state machine | Scattered status string comparisons |
| Need to represent a business operation | Command/use case | Command bus for trivial CRUD |
| Creating nontrivial immutable structures | Builder/factory | Factory for every constructor |
| Async post-commit processing | Transactional outbox | Publishing before database commit |
| Repeated requests | Idempotency keys/constraints | Memory-only deduplication for important writes |
| Resource overload | Limits/queues/backpressure | Infinite queues or retry storms |
| Repeated expensive reads | Cache-aside with invalidation | Adding caching without measurements |
| Cross-service business coordination | Saga/workflow | Saga inside one DB transaction |
| Read-heavy scaling | Optimize SQL, indexes, pagination first | Premature sharding and replication |

Any pattern must have a documented **problem**, **simpler alternative**, **new failure modes**, **test plan**, and **removal condition**.

## 7. Domain, state, data, and persistence [DATA]

### Business correctness

- Model important entities, transitions and invariants explicitly.
- Reject illegal transitions at the authoritative write boundary, not only in UI controls.
- Make authorization tenant- and object-aware for every sensitive operation.
- Keep transactional boundaries short and purposeful; use database constraints as a final correctness backstop.
- For money, define currency, units, rounding, tax/discount sequencing, and refund semantics; avoid binary floating point for financial amounts unless the representation is demonstrably safe.
- Define time zones, UTC storage conventions, and user-visible display expectations explicitly.

### Persistence

- Use schema migrations reviewed and tested against realistic data.
- Prefer safe expand/migrate/contract sequences for live schema transitions.
- Make uniqueness, referential integrity and nullability explicit at the database layer.
- Use parameterized SQL; never interpolate untrusted data into executable statements.
- Verify query plans and indexes on representative datasets before adding a cache.
- Use cursor/keyset pagination for large changing collections when appropriate.
- Design transaction isolation and locking according to concurrency invariants; test contested writes.
- Support safe retry after serialization conflicts where appropriate; avoid retrying non-idempotent external effects.
- Keep clear ownership for data retention, backup, recovery, deletion, and audit history.
- Test actual restore procedures, not only backup creation.

### API and contracts [SERVICE]

- Define versioning and compatibility policy before exposing public contracts.
- Use predictable status codes, validation details, error identifiers, and pagination semantics.
- Make request payload limits, timeout contracts, idempotency, and rate limits explicit.
- Authenticate callers; separately authorize each action against each resource.
- Prefer consistent typed schemas and generate clients when tooling reduces drift.
- Support forward/backward compatibility during rolling deployments.
- Never treat the UI's calculated amount as authoritative for a payment.

## 8. Concurrency and async work [SERVICE, DATA]

- Identify mutable shared state and specify ownership.
- Minimize lock duration and avoid holding locks across remote calls.
- Prefer bounded concurrency and queues; unlimited goroutines/tasks/promises are not a scalability strategy.
- Use transaction isolation, row locks, optimistic versions, and uniqueness according to documented invariants.
- Decide whether ordering is required per entity, per partition, globally, or not at all.
- Handle cancellation, duplicate delivery, out-of-order events, stalled jobs, worker crashes, and safe replay.
- Distinguish **at-most-once**, **at-least-once**, and **effectively-once business effects**; don't casually claim exactly-once distributed execution.
- Require idempotent consumers for at-least-once delivery.
- Prefer durable outbox/inbox patterns for important work spanning DB commit and external messaging.
- Test two or more workers competing for the same job and sudden process termination after each critical transition.

## 9. Resilience and distributed systems [SERVICE]

- Give every external operation an appropriate deadline; budgets should account for nested calls.
- Retry only failures with retryable semantics, with bounded attempts and exponential backoff plus jitter.
- Avoid layered retry multiplication; define where retries are owned.
- Use a circuit breaker when repeated calls to a failing dependency cause meaningful harm.
- Separate resource pools or use bulkheads where one dependency can exhaust shared capacity.
- Apply quotas/rate limits per actor/tenant as needed; protect queues with backpressure and load shedding.
- Degrade nonessential features before business-critical operations.
- Design health/readiness checks around actual instance readiness; avoid costly synchronous dependency checks on every probe.
- Plan graceful shutdown to drain or hand off work.
- Track delivery state, poison messages, dead letters, replay and reconciliation.
- For remote payments and irreversible operations, reconcile ambiguous outcomes instead of assuming timeout means failure.
- Record dependency outage behavior in runbooks and test using fault injection where risk justifies it.

**Avoid defaulting to:** Kafka, Redis, service meshes, microservices, multi-region active-active, read replicas or sharding without a quantified need and operations owner.

## 10. Security, privacy, and supply chain [ALL; controls proportionate to risk]

### Security by design

- Threat-model trust boundaries, sensitive assets, actors, and abuse scenarios.
- Default deny; grant least privilege for users, services, database roles, and CI runners.
- Use maintained authentication implementations. Never invent cryptographic algorithms.
- Enforce authorization server-side on every privileged and object-scoped operation.
- Validate and normalize untrusted inputs; encode outputs for the actual context. Use safe HTML sanitization only where HTML is intentionally allowed.
- Avoid SQL, shell, HTML, template, path, and command injection.
- Use secure session, cookie, CORS and CSRF policies appropriate to the client architecture.
- Require TLS for sensitive network links and encrypt sensitive storage according to threat model.
- Store secrets in appropriate secret managers or protected environment configuration, never source control, client assets, or logs.
- Collect minimal personal information; define data retention and deletion.
- Avoid PII or credentials in structured logs, traces and error payloads.
- Apply rate limits and abuse protection to costly or sensitive endpoints.
- Track dependencies, known vulnerabilities, licenses, source integrity, and update procedures.
- Lock dependency versions for reproducible builds; review changes to build scripts, CI workflows and generated artifacts.
- Prefer short-lived CI identities, restricted permissions, trusted runners, and provenance where appropriate.
- Plan vulnerability response and emergency patch procedures.

**Baseline references:** OWASP ASVS 5.0.0 (for applicable web/API controls), NIST SSDF 1.1, OWASP CI/CD Security Cheat Sheet, and SLSA 1.2 when build provenance matters.

## 11. Testing and verification [ALL]

### Test the intended contract

- Favor tests that fail when user-visible behavior, domain invariants, safety, or integrations break.
- Use fast deterministic unit tests for pure logic.
- Use integration tests for databases, serialization, queues, auth providers, and external adapters; mocks alone are insufficient to verify integration contracts.
- Keep a small set of critical end-to-end journeys; do not drive every trivial branch through a browser.
- Prefer stable assertions over implementation-coupled expectations.
- Use descriptive scenarios, clear fixtures, and reproducible environments.
- Test success, invalid input, missing permissions, retries, timeouts, cancellation, concurrency, and recovery as applicable.
- Use property-based, fuzz, or mutation testing where input spaces and invariants justify the cost.
- Treat flaky tests as defects; quarantine only with an owner and deadline.
- Test migration upgrade/rollback or recovery strategies with representative data.
- Add a regression test for each material bug when practical.
- Avoid arbitrary coverage percentages as the only quality gate. Risk-weighted branch and behavior coverage is more valuable.

### Test selection matrix

| Change | Minimum meaningful verification |
| --- | --- |
| Pure function | Focused unit tests including edge cases |
| New business invariant | Domain tests + authoritative write-path test |
| Database query/migration | Real-database integration test + realistic data |
| External API contract | Contract/integration test + failure behavior |
| Authentication/authorization | Allowed and forbidden actor/resource combinations |
| Concurrent workflow | Parallel execution, duplicate and crash/recovery cases |
| UI behavior | Accessible interaction test + key end-to-end flow |
| Performance change | Representative before/after benchmark with methodology |
| AI prompt/model/router change | Versioned evaluation suite, negative cases, cost/latency and safety checks |

**TDD:** Useful for difficult behavior and regressions, not a universal requirement that every line must be written after a test. Keep test code readable; duplication in tests can improve clarity.

## 12. Performance and scalability [ALL, AT SCALE]

- Start with realistic budgets for latency, memory, CPU, I/O, startup, energy, and cost relevant to the product.
- Profile before optimizing. Establish reproducible baselines and representative test data.
- Fix algorithmic and query inefficiencies before introducing infrastructure.
- Avoid N+1 queries, unnecessary allocations, overfetching, repeated network round trips and unbounded memory growth.
- Batch safely where it reduces overhead without harming latency or fairness.
- Use pagination, streaming, bounds, and cancellation to cap resource use.
- Distinguish latency percentiles (p50/p95/p99), throughput, saturation, and tail behavior.
- Cache only with a documented consistency model, TTL/invalidation, key ownership, privacy boundaries, and fallback.
- Add load balancing and replicas when capacity/availability goals require multiple instances.
- Shard only after indexing, query design, partitioning, maintenance, and scaling measurements justify it.
- Benchmark optimized paths and check regressions on realistic workloads.

## 13. User experience and accessibility [UI]

- Favor intuitive flows, predictable states, clear feedback, and recoverable errors.
- Design loading, empty, error, offline, retry, and partial-success states explicitly.
- Do not show optimistic UI as a confirmed financial or durable operation.
- Protect users from duplicate submissions without depending solely on disabled buttons.
- Provide keyboard access, semantic labels, visible focus, meaningful text alternatives, contrast, and screen-reader-compatible status updates.
- Evaluate applicable WCAG 2.2 A/AA criteria where web accessibility requirements apply.
- Localize dates, numbers, currency, time zones, reading direction, and meaningful text where the audience requires it.
- Avoid unnecessary animations, hidden destructive actions, or ambiguous error messages.
- Minimize costly client-side computation and ship appropriate assets efficiently.

## 14. Observability and operations [SERVICE; other products as applicable]

- Instrument meaningful operations with structured logs, metrics, and traces or equivalent diagnostics.
- Prefer OpenTelemetry conventions when they aid interoperability; don't force a costly telemetry stack on a standalone script.
- Carry correlation/request IDs across inbound request, database operations, jobs, and external dependencies.
- Record errors with causes and useful context while redacting sensitive details.
- Distinguish technical health from customer experience through SLIs/SLOs where meaningful.
- Alert on actionable symptoms: user-visible errors, latency, saturation, stuck jobs, payment reconciliation gaps and data integrity issues.
- Define owners, severity, escalation, runbooks, dashboards, and rollback paths.
- Maintain tested backups and restoration objectives for critical data.
- Review incidents without blame; convert findings into controls and regression tests.

## 15. Build, CI, delivery, and dependencies [ALL]

### Reproducibility

- Version control source, build scripts, schema changes, and infrastructure declarations.
- Lock or otherwise record dependency resolution where supported.
- Separate build, release, and runtime concerns; keep secrets out of build artifacts.
- Prefer one documented bootstrap and verification command per repository.
- Keep local and CI toolchain versions consistent with production where important.
- Enforce formatting and static checks automatically; do not make reviewers police whitespace.
- Scope checks by changed files/modules when correct, but retain periodic full-repository verification.

### Fast and trustworthy feedback

- Optimize **feedback loop time**, not merely the runtime of one command.
- Separate fast PR gates from broader nightly or pre-release suites while keeping critical protection on the merge path.
- Cache only reproducible and safely isolated artifacts; prevent cross-branch or untrusted PR cache poisoning.
- Minimize CI queue delays and redundant network setup; use parallelism after measuring contention.
- Require branch protection, review, and explicit ownership for privileged or destructive releases.
- Make deployments reversible through backward-compatible changes, controlled rollout and rollback.
- Use feature flags for real release-control requirements; remove stale flags promptly.
- Evaluate delivery using throughput **and** stability, not raw deployment frequency alone.

### Dependencies

- Prefer fewer mature dependencies to many tiny wrappers when risk, maintenance and license burden are lower.
- Define the reason for major dependencies and maintain an update path.
- Keep package graph lean; remove abandoned components and unused transitive dependencies where possible.
- Pin CI actions and sensitive build inputs appropriately; control who can modify pipelines.

## 16. Documentation and decisions [ALL]

Keep documentation proportional and accurate:

- `README`: purpose, quick start, exact commands, config, architecture entry points.
- API/schema docs: behavioral contracts, auth, error conditions, versioning.
- `CONTRIBUTING`: workflow, tests, formatting and review expectations.
- `SECURITY`: reporting process, access controls and operational safeguards where relevant.
- Architecture diagram: only when it improves comprehension; update it when topology changes.
- `ADR`s: consequential choices, context, alternatives, tradeoffs, status and reversal triggers.
- Runbooks: how to detect, mitigate, diagnose and restore real failures.
- Documentation near code for invariants and non-obvious constraints.

Remove or update stale claims. An ADR that describes an intended pattern is not proof that it works; link to relevant code and executable tests.

## 17. AI/ML and coding-agent safeguards [AI]

### AI-enabled applications

- Use a deterministic program for operations that do not need a model.
- Choose the simplest workable orchestration: direct call → bounded workflow → specialist agent only if measured improvement justifies it.
- Treat retrieved documents, web pages, tool responses and repository files as **untrusted data**, not elevated instructions.
- Give agents least-privilege capabilities, explicit action scopes, short-lived credentials and human approval for consequential irreversible actions.
- Validate tool arguments and outputs with schemas plus authorization, not just model confidence.
- Limit tokens, tools, recursion, wall time, spend, retries and side effects.
- Track model versions, prompts, evaluations, latency, costs and regressions.
- Separate model judgments from enforceable business/security policies.
- Evaluate on representative, adversarial and out-of-distribution cases; guard against data leakage between training and evaluation.
- Preserve user privacy and data provenance; do not log sensitive prompts or training data indiscriminately.
- Make state-changing tools idempotent or reconcile uncertain results.

### Coding agents in a repository

1. Inspect existing architecture, conventions and similar implementation before editing.
2. State objective, constraints, risk and success criteria.
3. Reuse current patterns and commands unless there is concrete evidence they are inadequate.
4. Implement the smallest coherent diff; avoid speculative abstractions, drive-by refactors and unrelated dependency changes.
5. Add tests at the actual failure boundaries, especially auth, concurrency and persistence.
6. Run formatting, static analysis, relevant tests and integration checks.
7. Re-check the changed code for hidden side effects, security boundary violations, API drift, stale comments and orphaned code.
8. Report what changed, what tests ran, what passed or failed, and what remains unverified. Never invent test results.
9. Ask for confirmation before destructive or irreversible external actions.
10. Provide evidence for architectural recommendations; mark existing vs missing vs not applicable vs justified deferral.

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

### Definition of done

A change is done when its intended behavior is documented or obvious, its acceptance criteria are satisfied, critical failure paths are addressed, relevant tests pass, security is preserved, observability and rollout needs are handled, and reviewers can understand and maintain it.

## 19. Anti-patterns and better alternatives

| Anti-pattern | Why it harms | Better approach |
| --- | --- | --- |
| Speculative abstraction | Extra layers and frozen assumptions | Concrete solution; extract when variation is known |
| God class/service | Mixed responsibilities and risky edits | Cohesive feature modules and focused collaborators |
| Interface per function | Indirection without benefit | Concrete functions; interfaces at real boundaries |
| Generic repository for all tables | Obscures queries and constraints | Task/aggregate-specific persistence |
| Distributed monolith | Service overhead without independence | Modular monolith or clean service ownership |
| Microservices by default | Operational and consistency overhead | Split only with demonstrated needs |
| Event sourcing for audit only | Costly evolution and replay | State plus suitable audit log |
| Cache before profiling | Staleness and invalidation complexity | Query fixes, then measured cache |
| `try/catch` and ignore | Data loss and silent failures | Explicit error propagation and observability |
| Retry everything | Duplicate writes and retry storms | Bounded, classified, idempotent retries |
| Endless queues | Memory exhaustion and unbounded delays | Backpressure, caps, DLQ and overload policy |
| Unit-test mocks only | Fails to catch integration bugs | Real database and contract tests |
| 100% coverage obsession | Brittle low-value tests | Risk-weighted behavior/invariant testing |
| Snapshot every UI state | Tests unrelated markup changes | Semantic and accessible behavior tests |
| Logging everything | Noise, cost, privacy exposure | Structured actionable signals and redaction |
| Feature-flag graveyard | Exponential behavioral combinations | Owners, expiry, cleanup |
| Premature optimization | Complexity without user benefit | Measure, optimize, benchmark |
| Lint/style wars | Distracts from correctness | Autoformat and automated lint |
| Giant PRs | Slow feedback and poor review | Small coherent changes |
| Changing code just to match a diagram | Cosmetic churn and bugs | Audit behavior and change only where justified |
| Agent-written tests that always pass | False confidence | Assert meaningful behavior and inject failure cases |

## 20. Adoption roadmap and scorecard

### Phase 0 — Inventory, not refactor

- Identify supported language/runtime, app type, entry points, deployments, data stores, dependencies, tests, CI, sensitive operations and owners.
- Read code and test evidence; mark items **Implemented / Partial / Missing / Not applicable / Deferred (justification)**.
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

### Suggested scoring rubric (per applicable control)

- **0 = absent and required**
- **1 = partial / manual / unverified**
- **2 = implemented and tested**
- **N/A = legitimately irrelevant**
- **Deferred = needed only after documented trigger**

Prioritize by expected harm × likelihood × user impact, not by counting design patterns or maximizing a score.

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

### New infrastructure or design pattern

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
- [ ] Final report distinguishes verified, inferred, deferred and unknown claims.

## 22. Research sources

Primary or authoritative references (accessed 2026-11-01):

1. Martin Fowler, *Yagni*: https://martinfowler.com/bliki/Yagni.html
2. Martin Fowler, *Beck Design Rules*: https://martinfowler.com/bliki/BeckDesignRules.html
3. Google, *Engineering Practices / Code Review*: https://google.github.io/eng-practices/review/
4. Google, *What to look for in a code review*: https://google.github.io/eng-practices/review/reviewer/looking-for.html
5. Google, *Small changelists*: https://google.github.io/eng-practices/review/developer/small-cls.html
6. Martin Fowler, *Practical Test Pyramid*: https://martinfowler.com/articles/practical-test-pyramid.html
7. OWASP, *ASVS 5.0.0*: https://asvs.owasp.org/
8. NIST, *Secure Software Development Framework*: https://csrc.nist.gov/projects/ssdf
9. OWASP, *CI/CD Security Cheat Sheet*: https://cheatsheetseries.owasp.org/cheatsheets/CI_CD_Security_Cheat_Sheet.html
10. OpenSSF, *SLSA v1.2*: https://slsa.dev/spec/v1.2/
11. Microsoft, *Cloud Design Patterns*: https://learn.microsoft.com/en-us/azure/architecture/patterns/
12. AWS, *Timeouts, Retries, Backoff, and Jitter*: https://builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter
13. OpenTelemetry, *Semantic Conventions*: https://opentelemetry.io/docs/concepts/semantic-conventions/
14. Google SRE, *Production Services Best Practices*: https://sre.google/sre-book/service-best-practices/
15. DORA, *Software Delivery Performance Metrics*: https://dora.dev/guides/dora-metrics/
16. The Twelve-Factor App: https://12factor.net/
17. W3C, *Web Content Accessibility Guidelines 2.2*: https://www.w3.org/TR/WCAG22/
18. OWASP, *Top 10 for LLMs*: https://genai.owasp.org/llm-top-10/
19. OWASP, *Agentic AI Security*: https://genai.owasp.org/2025/12/09/owasp-genai-security-project-releases-top-10-risks-and-mitigations-for-agentic-ai-security/

**Interpretation note:** This guide synthesizes and operationalizes these sources. Its P0–P3 priorities and acceptance criteria are recommendations, not official mandates or a one-size-fits-all compliance certification. Security and regulatory obligations may impose additional requirements.
