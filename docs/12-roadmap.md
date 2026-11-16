# 12 — Roadmap: upgrade the lab without rewriting history

The existing case study is **complete as a verified GitOps rollout demonstration**. The items below are future enhancements, not retroactively completed achievements.

## Priority 0 — Security and account hygiene

- [ ] Verify AWS access key involved in an earlier screenshot was revoked/rotated and usage audited.
- [ ] Verify Argo CD initial admin password rotation; prefer a dedicated SSO identity.
- [ ] Review EKS endpoint accessibility and restrict public API CIDRs as appropriate.
- [ ] Audit GitHub OIDC IAM trust and least-privilege ECR permissions.

## Priority 1 — Reliability exercises

- [ ] Enforce desired Pod separation with tested node/zone scheduling policy.
- [ ] Define a PodDisruptionBudget and observe controlled node drain behavior.
- [ ] Run a fully evidenced Git-based rollback.
- [ ] Run a safe drift/self-healing exercise and capture before/after states.

## Priority 2 — Deployment hardening

- [ ] Enforce ECR tag immutability / digest pinning.
- [ ] Add vulnerability scanning and optional provenance attestations.
- [ ] Add NetworkPolicy and repository branch-protection/reviewer requirements.
- [ ] Verify topology-aware capacity and resource scheduling under load.

## Priority 3 — Optional public exposure

- [ ] Select ingress/load-balancer design and validate subnet routing/controller requirements.
- [ ] Add TLS certificate, DNS and an appropriate HTTPS entry point.
- [ ] Verify public endpoint access from a separate network.
- [ ] Document external exposure threat model and WAF/rate limits where relevant.

## Priority 4 — Observability and recovery

- [ ] Add structured application logs and useful request/latency metrics.
- [ ] Configure dashboards and alerts with Prometheus/Grafana or AWS equivalents.
- [ ] Test node failure, deployment rollback and any data backup restore.
- [ ] Add a real incident exercise with timeline and recovery measurements.

The repository should update its README **only when proof for each new achievement exists**. No future feature should be marketed as already implemented.
