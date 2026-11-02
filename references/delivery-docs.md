# Build, CI, delivery, dependencies, and documentation [ALL]

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
