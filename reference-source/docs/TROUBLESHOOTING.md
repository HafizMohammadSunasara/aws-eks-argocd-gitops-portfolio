# Troubleshooting playbook

These are **possible problems to diagnose**, not claims that they happened in this new project. Capture actual command output and timestamps when a future error occurs.

| Symptom | Likely area | First checks |
| --- | --- | --- |
| GitHub Actions red at Python tests | App code/test dependency | Read failed step; install `requirements-dev.txt`; rerun `python -m unittest discover -s tests -v`. |
| GitHub Actions Docker build red | Dockerfile / dependency install | Read build log, check Docker daemon and pinned package releases. |
| ECR publish job skipped | AWS not configured yet | On first upload this is expected. Later verify repository variables `AWS_REGION`, `AWS_ROLE_ARN`, `ECR_REPOSITORY`. |
| `AccessDenied` assuming AWS role | GitHub OIDC trust/policy | Check provider audience, exact repo and branch `sub`, role ARN, `id-token: write`. |
| `403` or denied ECR push | Missing ECR repository/permissions | Confirm correct account/region/repository, IAM role permissions, auth, image tag. |
| No GitOps promotion PR created | GitHub workflow permissions | Enable create-PR setting; check action job token scope; verify manifest changed. |
| EKS node group stuck / `NodeCreationFailure` | Node IAM, subnet routing, DNS, security groups | Inspect EKS health events, node role and private subnet outbound access. |
| `kubectl` unauthorized | EKS access entry/RBAC or wrong cluster | `kubectl config current-context`, `aws sts get-caller-identity`, verify EKS access entries. |
| Argo CD app OutOfSync | Git diff waiting for sync | Examine Application source/path/branch and diff; check manual vs automated policy. |
| `ImagePullBackOff` | ECR image not present/node IAM | Inspect `kubectl describe pod`, ensure manifest SHA exists in ECR and node role can pull. |
| Pod not Ready / CrashLoopBackOff | Flask app, image, health probe | `kubectl logs`, `kubectl describe pod`; verify `/readyz`, port 8080, resources. |
| Two Pods on same worker | Best-effort spreading only | `kubectl get pods -o wide`; topology `ScheduleAnyway` is a preference, not guarantee. |
| `LoadBalancer` pending | AWS LB Controller or subnet discovery | Controller Pods/logs, proper IAM, public subnet tags and IGW route. |
| NLB created but Internal | Wrong scheme or subnet selection | Validate internet-facing annotation and public-subnet selection. |
| NLB hostname exists, browser timeout | Targets/listener/security group/routing | Target group health, Service endpoints, listener port 80, public routing. |

Useful diagnostic commands (only **after** configuring access to the correct EKS cluster):

```bash
aws sts get-caller-identity
kubectl config current-context
kubectl get nodes -o wide
kubectl get pods -A
kubectl describe deployment gitops-flask -n gitops-demo
kubectl get pods -n gitops-demo -o wide
kubectl logs deployment/gitops-flask -n gitops-demo --tail=100
kubectl get svc -n gitops-demo -o wide
kubectl get events -n gitops-demo --sort-by=.lastTimestamp
kubectl get applications -n argocd
```

**Debugging rule:** A green CI pipeline proves a build passed, not necessarily that the app is reachable. Verify independently: image exists → two Nodes Ready → two Pods Ready → Argo Synced/Healthy → NLB targets healthy → browser HTTP response.
