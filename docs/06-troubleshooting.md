# 06 — Debugging casebook: observed failures and safe conclusions

Real troubleshooting is valuable only when evidence and interpretation are separated.

## Case 1 — Argo CD was OutOfSync / Missing

**Observed:** After the Argo Application manifest was applied, the app appeared \`OutOfSync\` and \`Missing\`.

**Action shown:** A sync operation was requested for the Git target revision; the status was queried again.

**Observed after:** \`Synced / Healthy\`, Deployment available 2/2, two Running Pods, ClusterIP Service.

**Evidence:** [Initial and resolved state](../evidence/screenshots/04-initial-sync-recovery.png), [HTTP checks](../evidence/screenshots/05-health-ready-checks.png).

**Lesson:** Application registration and reconciliation can be separate operations, and an intermediate status isn't final success or failure.

## Case 2 — GitHub Actions had a red run

**Observed:** Run #19 showed a failed workflow. Later runs passed.

**What the record proves:** There was at least one failure followed by later successful checks and release promotion.

**What it does not prove:** An exact exception, YAML parser error, missing IAM permission or Docker failure as the root cause. Those would require failed-job logs, which are not established by the status-list screenshots alone.

**Evidence:** [Red run history](../evidence/screenshots/06-historical-ci-failure.png) → [green run](../evidence/screenshots/07-ci-green-after-fix.png).

**Lesson:** Always distinguish the green outcome from the causal explanation.

## Case 3 — Windows port-forward on 8080 failed

**Observed command:**

\`\`\`powershell
kubectl -n argocd port-forward svc/argocd-server 8080:443
\`\`\`

Windows reported a bind/listener permission error on \`127.0.0.1:8080\` and \`[::1]:8080\`.

**Safe workaround:**

\`\`\`powershell
kubectl -n argocd port-forward --address 127.0.0.1 svc/argocd-server 18080:443
\`\`\`

**Result:** The alternate local port forwarded successfully, and Argo CD login/dashboard loaded at \`https://localhost:18080\`. A certificate warning can be expected with a self-signed local tunnel endpoint; do not disable security controls on unrelated sites.

**Evidence:** [Error](../evidence/screenshots/11-windows-port-8080-error.png) → [working forward](../evidence/screenshots/12-alternative-port-forward-working.png).

**Lesson:** Local host port binding is not evidence of a cluster outage.

## Case 4 — Kubernetes namespace RBAC rejected a Service read

**Observed:** One PowerShell attempt returned \`Forbidden\` for \`services\` in \`gitops-demo\`, identifying the AWS IAM user.

**Interpretation:** AWS identity authentication worked, but Kubernetes authorization for that verb/resource/namespace was not granted to that principal.

**Correct diagnostic route:** Inspect EKS access entries, IAM mapping and Role/RoleBinding or ClusterRoleBinding; grant the minimal required permissions and re-test with \`kubectl auth can-i get services -n gitops-demo\`.

**Security decision:** The original captured terminal also revealed an Argo CD initial admin password. It is excluded from the public evidence pack. A later successful port-forward screenshot is a different observation; it does not prove the exact RBAC fix performed.

## Case 5 — A successful PR job had 'publish skipped'

The ECR publish job contains an event condition restricting execution to \`push\`. On PR validation it was **supposed** to skip. The workflow still completed successfully.

**Evidence:** [Intentional skip](../evidence/screenshots/08-intentional-pr-publish-skip.png).

**Lesson:** Check job \`if:\` conditions before calling a skipped action a bug.

## A reusable debugging method

1. Record the exact error, component, event and time.
2. Identify the system boundary: workstation, GitHub runner, AWS auth, ECR, Argo CD, Kubernetes API, Pod or HTTP.
3. Run the least-invasive read-only check for that layer.
4. Change one parameter or policy at a time and re-test.
5. Record before/after output and identify remaining uncertainty.
6. Never paste secrets or tokens into a publicly shared screenshot.
