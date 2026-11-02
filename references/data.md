# Data, state, and concurrency [DATA]

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
