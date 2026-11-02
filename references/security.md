# Security, privacy, and supply chain [ALL]

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
