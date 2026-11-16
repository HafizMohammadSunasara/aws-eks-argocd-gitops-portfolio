# Security policy for this public engineering portfolio

This is a public **case study**, not a password vault, cluster configuration backup, or production deployment endpoint.

## Material intentionally excluded

- AWS Access Key ID and Secret Access Key shown in an earlier local PowerShell screenshot.
- Argo CD bootstrap admin password shown in earlier terminal captures.
- Kubeconfig, local AWS credentials, active session cookies, secrets and personal account exports.
- Screenshots displaying those credentials, even when otherwise useful as debugging evidence.

**Publication does not undo past exposure.** The credential owner should revoke/rotate the exposed AWS access key and Argo CD password, review relevant access logs, and verify no copy reached Git history or other public surfaces. This portfolio makes no unverified claim that a complete credential incident review occurred.

## Safe evidence

The 16 screenshots under \`evidence/screenshots/\` were selected for technical value and screened for key/password strings. Some captures still display AWS account identifiers, node hostnames or cluster names that appear in the original public project. Those are identifiers, **not** authentication secrets. Review privacy preferences before publishing.

## Scope and residual risk

- The original workflow uses GitHub OIDC role assumption for ECR access.
- The live application has an internal Kubernetes ClusterIP Service, not a public URL.
- EKS public API endpoint restrictions, least-privilege IAM, Kubernetes RBAC, provenance scanning, NetworkPolicy, TLS, monitoring and failure-domain spread all deserve periodic review.
- \`reference-source/k8s/optional/public-nlb-service.yaml\` is optional and not evidence of a live public NLB.
- Do not treat the reference snapshot as a production deployment automation or use it with unreviewed credentials.

If you discover a vulnerability, contact the owner privately through a verified channel. Do not paste credentials in public GitHub Issues.
