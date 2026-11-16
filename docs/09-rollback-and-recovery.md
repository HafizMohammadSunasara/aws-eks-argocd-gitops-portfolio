# 09 — Rollback and drift recovery: a controlled exercise plan

**Status: Proposed exercise; not represented as a completed result.** The successful lab proves forward rollout of an updated image. A real rollback claim needs the same quality of before/after evidence.

## Why Git rollback?

If Git is the declared source of truth, a durable rollback should change the desired image in Git. A direct \`kubectl set image\` may quickly change a Pod template, but Argo CD can later reconcile the cluster back to what Git still requests.

## Safer version-promotion rollback

1. Record the currently deployed source SHA and registry image digest.
2. Select a previously tested image, confirm it still exists in ECR.
3. Create a branch and change **only** \`k8s/overlays/dev/kustomization.yaml\` to the older tested SHA.
4. Review tests, policy and manifest diff in a pull request.
5. Merge the PR; do **not** use the CI runner as the deployment actor.
6. Observe Argo CD syncing the updated desired state.
7. Check Deployment rollout, Ready replicas, \`/healthz\`, \`/readyz\` and the browser heading.
8. Archive commit, PR, ECR digest, Argo sync and post-rollback HTTP evidence.

## Drift test design

A drift test changes a safe field on a controlled non-production resource, confirms Argo marks drift, then confirms self-healing returns it to the Git desired state. Avoid testing uncontrolled destructive drift on production workloads.

### Checkpoints

| Phase | Proof to capture |
|---|---|
| Baseline | Argo Synced/Healthy and current image SHA |
| Drift | Live-vs-Git diff visible |
| Recovery | Argo reconciles without ad hoc intervention |
| Final | Restored Git-desired image/config and HTTP health |

## Recovery and blast radius

Do not confuse rolling back an application image with disaster recovery. EKS control-plane availability, node replacement, EBS data backups, cluster recreatability and IAM compromise response are separate concerns.
