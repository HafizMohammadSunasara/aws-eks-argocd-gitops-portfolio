# 08 — Security, identity and trust boundaries

## GitHub → AWS: OIDC instead of long-lived runner keys

The CI workflow uses GitHub's \`id-token: write\` permission and the AWS credential action to assume a role. This provides temporary AWS credentials for ECR publishing. AWS role trust and least-privilege policy still require maintenance; a valid identity token must not be accepted from arbitrary repositories/branches.

The workflow grants the publishing job \`contents: write\`, \`pull-requests: write\` and \`id-token: write\` because it must open the promotion PR and push an image. Consider whether repository-specific permission boundaries can be tightened further.

## AWS → EKS: authentication does not equal authorization

An AWS CLI \`sts get-caller-identity\` success only shows who AWS believes the caller is. Kubernetes authorization then decides whether that caller may read \`services\`, list Pods, manage Deployments, or establish port-forward connections in a namespace.

The recorded \`Forbidden\` error in \`gitops-demo\` demonstrates this boundary. Review EKS access policies, Kubernetes RBAC and scope—not blanket admin privileges—as the fix.

## Container and workload controls

Observed in the original manifests:

| Control | Configuration |
|---|---|
| Non-root | UID/GID 10001 |
| Privilege escalation | Disabled |
| Linux capabilities | All dropped |
| Root filesystem | Read-only |
| Seccomp | RuntimeDefault |
| Service account token | Automount disabled |
| Resource budget | CPU/memory requests and limits |
| Probes | Startup/readiness/liveness |
| Public service exposure | No; ClusterIP in deployed app |

None of these by itself constitutes a full security audit.

## Credential-exposure incident

During troubleshooting, screenshots showed an AWS access-key pair and a decoded Argo CD initial admin password. Those captures are **not** inside this repository. Deleting screenshots is not sufficient: the affected AWS key and Argo password should be rotated/revoked, relevant logs reviewed, and public Git history inspected for copied credential text.

Do not repeat the original secret values in reports, commit messages or issues.

## Open hardening items

- Tighten EKS public API endpoint CIDR/access according to operator needs.
- Audit AWS role trust conditions and ECR repository policy.
- Prefer digest-pinned or enforced immutable tags, image scanning and signed provenance.
- Add egress/ingress NetworkPolicy if the cluster network plugin supports it.
- Add RBAC tests and automated security checks.
- Confirm encryption, logs, TLS/DNS and monitoring.

For safe publication rules see [SECURITY.md](../SECURITY.md).
