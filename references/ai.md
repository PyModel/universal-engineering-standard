# AI-enabled applications [AI]

## 17. AI/ML application safeguards [AI]

Coding-agent safeguards: SKILL.md §3.

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
