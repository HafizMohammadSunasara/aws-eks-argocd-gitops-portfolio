# Evidence index — 16 selected screenshots

**Source:** User-provided captures from 15 November 2026. Original filenames had the form \`image(20261115-HHMMSS).png\`; files below are renamed copies. Evidence is ordered by explanation, not a claim that every screen capture came from a separate deployment.

The original high-risk PowerShell screenshots containing AWS long-lived credentials and an Argo CD admin password have been **excluded**, not hidden in a zip subfolder. A public GitHub URL or screenshot is not a live-app availability guarantee.

| # | File | Original timestamp | What it demonstrates | Interpretation |
|---|---|---|---|---|
| 01 | [EKS node group](screenshots/01-eks-nodegroup-active.png) | 161741 | Managed worker group Active | Infrastructure readiness |
| 02 | [2 worker nodes](screenshots/02-two-worker-nodes-ready.png) | 171241 | Two nodes Ready | Does **not** prove automatic multi-AZ pod spread |
| 03 | [Argo components](screenshots/03-argocd-components-running.png) | 174002 | Argo system components running | Controller installation |
| 04 | [Initial sync recovery](screenshots/04-initial-sync-recovery.png) | 174427 | OutOfSync/Missing → sync and healthy state | Shows transition; no invented stack trace |
| 05 | [Health/readiness](screenshots/05-health-ready-checks.png) | 174952 | HTTP health and readiness check outputs | Internal service behavior |
| 06 | [CI red run](screenshots/06-historical-ci-failure.png) | 175646 | Prior failed GitHub Actions run | Exact root cause requires job logs |
| 07 | [CI green run](screenshots/07-ci-green-after-fix.png) | 175914 | Later successful workflow | Evidence of subsequent passing run |
| 08 | [PR publish skipped](screenshots/08-intentional-pr-publish-skip.png) | 180448 | Publish job skipped on PR | Expected \`push\`-only gate, not failure |
| 09 | [Merged promotion PR](screenshots/09-promotion-pr-merged.png) | 180811 | Review/merge of image-promotion PR | GitOps release approval |
| 10 | [Image rollout](screenshots/10-immutable-image-rollout.png) | 180954 | New ECR SHA image in Deployment | Promotion reached Kubernetes |
| 11 | [Local port error](screenshots/11-windows-port-8080-error.png) | 182832 | Windows 8080 listener bind error | Debugging event |
| 12 | [Alternative port](screenshots/12-alternative-port-forward-working.png) | 183110 | 18080 forwarding successful | Local access remediation |
| 13 | [Argo dashboard](screenshots/13-argocd-dashboard-healthy.png) | 183335 | App Healthy/Synced | Controller status |
| 14 | [Argo resource tree](screenshots/14-argocd-resource-tree.png) | 183532 | Service/Deployment/ReplicaSets/Pods | Runtime topology |
| 15 | [Before update](screenshots/15-flask-before-change.png) | 184631 | Previous application heading | Before state |
| 16 | [Version 2](screenshots/16-flask-version-2-success.png) | 185136 | New heading and healthy app via localhost | After state |

## Critical cross-checks

- Original working repository: https://github.com/HafizMohammadSunasara/aws-eks-argocd-gitops
- Code revision promoted to ECR: \`1eda2123ef3b57054ac444f4842f60438e5d5571\`
- Approved promotion: https://github.com/HafizMohammadSunasara/aws-eks-argocd-gitops/pull/3
- Successful workflow runs: [#22](https://github.com/HafizMohammadSunasara/aws-eks-argocd-gitops/actions/runs/43748702205), [#23](https://github.com/HafizMohammadSunasara/aws-eks-argocd-gitops/actions/runs/43748769127)

## What's intentionally missing?

No screenshots are offered as proof of a production incident, public NLB/HTTPS endpoint, enforceable high availability, tested Git rollback, or completed cluster destruction. Those achievements were not demonstrated in the supplied final evidence.
