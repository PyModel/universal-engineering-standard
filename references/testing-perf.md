# Testing, verification, and performance [ALL]

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
