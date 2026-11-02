# Services: resilience and operations [SERVICE]

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
