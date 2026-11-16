# 01 — Project overview and the definition of done

**Project:** GitOps with Argo CD on Amazon EKS  
**Engineer:** Hafiz Mohammad Sunasara  
**Source:** [aws-eks-argocd-gitops](https://github.com/HafizMohammadSunasara/aws-eks-argocd-gitops)  
**Evidence date:** 15–16 November 2026 (local session timestamps)

## Business-like problem statement

Deploying containers through a one-off CLI command is difficult to audit. A CI platform that writes directly to Kubernetes can also blur responsibility between software build and infrastructure reconciliation. This lab explored a more reviewable path: create the image after tests, request an explicit version promotion through Git, and let a dedicated GitOps controller apply it.

The app is deliberately small—a Flask status page—so the main engineering subject stays on the **delivery system**, not front-end complexity.

## Built components

1. Python Flask application with \`/\`, \`/healthz\`, \`/readyz\` and \`/version\`.
2. Docker image and Python tests.
3. GitHub Actions CI and conditional Amazon ECR publish.
4. AWS OIDC role assumption for publishing.
5. Kubernetes base Deployment/Service and dev Kustomize overlay.
6. Argo CD Application monitoring \`main\` → \`k8s/overlays/dev\`.
7. An EKS cluster with two managed worker nodes.
8. GitHub image-promotion pull requests.
9. Final changed UI served from a new healthy Pod through local port-forward.

## Success conditions and proof

| Condition | Outcome | Evidence |
|---|---|---|
| EKS usable | Active, 2 Ready workers | [Nodes](../evidence/screenshots/02-two-worker-nodes-ready.png) |
| Argo CD installed | Components Running | [Controller Pods](../evidence/screenshots/03-argocd-components-running.png) |
| Application deployed | Healthy and Synced | [Dashboard](../evidence/screenshots/13-argocd-dashboard-healthy.png) |
| Container usable | Two Ready replicas in recorded check | [CLI](../evidence/screenshots/05-health-ready-checks.png) |
| App HTTP behavior | \`ok\` and \`ready\` | [HTTP probes](../evidence/screenshots/05-health-ready-checks.png) |
| CI and promotion | Successful runs and merged PR | [Run #22](https://github.com/HafizMohammadSunasara/aws-eks-argocd-gitops/actions/runs/43748702205) · [PR #3](https://github.com/HafizMohammadSunasara/aws-eks-argocd-gitops/pull/3) |
| Changed version live | Final Version 2 heading | [Browser capture](../evidence/screenshots/16-flask-version-2-success.png) |

## Exclusions and why they matter

- **Not a public web hosting project.** The Flask Service is \`ClusterIP\`; the demonstrated browser uses a localhost tunnel.
- **Not a tested failover claim.** Having two nodes is not the same as a completed cross-AZ resilience experiment.
- **Not a completed rollback exercise.** The Git-based rollback procedure is described, but its execution is future work.
- **Not a full DevSecOps product.** Core hardening is present; comprehensive scanning and monitoring are next-phase work.

## Reading order

Begin with [DEEP-DIVE.md](../DEEP-DIVE.md) for the full reasoning. Use the numbered docs for implementation details, then the [evidence index](../evidence/INDEX.md) to inspect claims directly.
