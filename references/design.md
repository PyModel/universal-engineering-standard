# Design and code [ALL]

Principles, SOLID, readable code, architecture, pattern selection, anti-patterns.

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
