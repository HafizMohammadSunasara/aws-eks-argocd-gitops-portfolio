# DEEP DIVE — GitHub Actions → ECR → Argo CD → Amazon EKS

> **A real lab implementation, explained from first principles to final verification.**  
> Author: Hafiz Mohammad Sunasara · November 2026 · Case-study commit: [\`fd9714f\`](https://github.com/HafizMohammadSunasara/aws-eks-argocd-gitops/commit/fd9714f7208c351340a471250dca940e90f2a38b)

This is the engineering record behind the black-and-gold portfolio. It intentionally distinguishes **observed**, **configured**, **demonstrated**, and **planned** behavior. The deployable application lives in the [original repository](https://github.com/HafizMohammadSunasara/aws-eks-argocd-gitops); this portfolio is a separate presentation repository.

## 01 — The problem: CI is not deployment state

Many beginner pipelines combine build, publish and \`kubectl apply\` into a single privileged job. That can work for a demo, but the CI runner becomes both the image builder **and** the Kubernetes deployment actor. Someone must now answer: *Who owns desired state? Who can approve a release? How do we reconstruct it or roll it back?*

The design here separates responsibilities:

- **GitHub Actions owns CI:** validate code/manifests, build the container, publish an immutable image.
- **Git owns desired release state:** a Kustomize overlay names the exact ECR image tag.
- **A promotion pull request provides a review boundary:** releasing a version is an explicit Git change.
- **Argo CD owns CD:** continuously compare Git with Kubernetes and apply desired changes.
- **EKS runs the workload:** the Kubernetes Deployment maintains the target replica count, with readiness/liveness probes.

The distinction is precise: **building an image is not a deployment**. Uploading to ECR does not automatically tell Kubernetes to run it. The GitOps PR is the link between those worlds.

## 02 — What ran, where?

| Component | Responsibility | Confirmed |
|---|---|---|
| GitHub \`main\` | Application and Kustomize desired state | Yes |
| GitHub Actions | Unit tests, YAML validation, Docker build, conditional publishing | Successful runs observed |
| AWS IAM role / GitHub OIDC | Short-lived workflow access to AWS | Workflow configuration and successful publish evidence |
| Amazon ECR | Stores SHA-tagged container images | Deployment image and promotion workflow verified |
| Argo CD | Watches \`k8s/overlays/dev\` on \`main\` | Application Synced / Healthy |
| Amazon EKS | Runs Kubernetes API and worker nodes | Cluster Active; 2 nodes Ready |
| Flask + Gunicorn | Serves the application and health endpoints | Running Pods and HTTP checks observed |
| ClusterIP Service | Exposes the workload internally | Verified; **no public Service endpoint** |

The implementation targeted AWS **\`us-east-1\`** and an EKS cluster named **\`gitops-eks-cluster\`**. Argo CD's app was named **\`gitops-flask-dev\`** and deployed into **\`gitops-demo\`**.

### The three control paths

1. **Source/control path:** GitHub \`main\` → GitHub Actions → ECR → promotion PR → merge.
2. **GitOps reconciliation path:** Argo CD polls/watches Git → reads Kustomize overlay → asks the Kubernetes API to reconcile the objects.
3. **Runtime/user path:** Browser on the operator's laptop → \`kubectl port-forward\` → ClusterIP Service → a healthy Flask Pod.

The last path is **local operator access**, not internet-facing hosting. Never substitute \`http://localhost:18081\` for a public demo URL in a job application.

## 03 — Infrastructure decisions

### EKS and worker capacity

Screenshots show the EKS cluster **Active**, a managed node group **Active**, and two worker nodes in the Kubernetes **Ready** state. Running two workers improves available capacity, but not automatically high availability: an application can still schedule both replicas to the same host or Availability Zone.

The Deployment in the application repository uses:

- \`replicas: 2\`
- \`RollingUpdate\`, \`maxSurge: 1\`, \`maxUnavailable: 0\`
- a **soft** topology spread constraint: \`whenUnsatisfiable: ScheduleAnyway\`

That is a thoughtful beginning, **not** an enforceable multi-AZ distribution guarantee. In one earlier capture the two Pods were on different nodes; later captures show both on one node. A production hardening step would review scheduling, failure domains and PodDisruptionBudget, then demonstrate behavior during node failure.

### Networking

The \`gitops-flask\` Service is type \`ClusterIP\` on port \`80\`, forwarding to container port \`8080\`. This protects the demo from accidental public exposure and explains why local port-forwarding was required.

An optional NLB manifest exists in the original app repo, but the final screenshots do **not** establish a publicly accessible NLB deployment. It is deliberately excluded from the 'completed' achievements.

### Container security

The manifest shows a non-root workload user (\`10001\`), Linux capability drops, no privilege escalation, a read-only root filesystem, \`RuntimeDefault\` seccomp, and disabled service-account-token automount. Gunicorn's temporary directory is supplied by an ephemeral \`emptyDir\` mount.

These are **configured hardening controls**. They don't prove a complete security assessment or compliance certification.

### Probes

Startup and liveness checks use \`/healthz\`; readiness uses \`/readyz\`. These are important because **Running** does not necessarily mean **ready to receive traffic**. The application returns simple JSON and an HTTP 200 when those checks succeed.

## 04 — The exact CI sequence

The source workflow is [\`.github/workflows/pipeline.yml\`](reference-source/.github/workflows/pipeline.yml) in the archived snapshot and [here in the working repo](https://github.com/HafizMohammadSunasara/aws-eks-argocd-gitops/blob/main/.github/workflows/pipeline.yml).

**Job 1: \`test\`**

1. Check out the repository.
2. Install Python 3.12.
3. Install application/test dependencies.
4. Run \`python -m unittest discover -s tests -v\`.
5. Run \`python scripts/validate_manifests.py\`.
6. Build a local Docker image as a packaging check.

**Job 2: \`publish\`**

This job depends on \`test\` and runs only on qualifying \`push\` events when \`AWS_REGION\`, \`AWS_ROLE_ARN\` and \`ECR_REPOSITORY\` repository variables are present.

1. Check out trusted \`main\`.
2. Exchange GitHub's OIDC token for AWS role credentials.
3. Authenticate Docker to ECR.
4. Build and push the image with the entire Git commit SHA as the tag.
5. Use \`scripts/update_image.py\` to change the Kustomize image declaration.
6. Use \`peter-evans/create-pull-request\` to propose the image-promotion PR.

An immutable Git-SHA tag is easier to trace than \`latest\`. A PR pointing at that tag links the requested deployment to a specific source revision. **Important nuance:** tags provide traceability but are not cryptographically immutable by themselves; ECR tag immutability policy and image digest verification provide stronger guarantees and are further hardening opportunities.

### Why a successful PR workflow can show 'publish skipped'

The publish condition only permits a \`push\` event, so a \`pull_request\` check may **correctly skip** the ECR publish job. The screenshot labeled [08](evidence/screenshots/08-intentional-pr-publish-skip.png) is evidence of event gating, not evidence of a broken pipeline.

### Why OIDC matters

The runner asks GitHub for an identity token, then assumes an IAM role instead of storing a long-lived AWS Secret Access Key in repository secrets. A good AWS trust policy scopes the allowed GitHub repository/ref, and the role policy permits only required ECR actions. This project had a credential-exposure incident in a local screenshot during troubleshooting; that screenshot was excluded from this public portfolio. Rotation and auditing must be managed separately from screenshot cleanup.

## 05 — Promotion is the deployment gate

The source app was changed to display:

> LIVE CI/CD PIPELINE DEMO — Version 2 - Powered by Amazon EKS.

The successful source change corresponds to commit [\`1eda2123ef3b57054ac444f4842f60438e5d5571\`](https://github.com/HafizMohammadSunasara/aws-eks-argocd-gitops/commit/1eda2123ef3b57054ac444f4842f60438e5d5571).

The workflow published the corresponding ECR image and opened [promotion PR #3](https://github.com/HafizMohammadSunasara/aws-eks-argocd-gitops/pull/3). Its merge produced source state [\`fd9714f7208c351340a471250dca940e90f2a38b\`](https://github.com/HafizMohammadSunasara/aws-eks-argocd-gitops/commit/fd9714f7208c351340a471250dca940e90f2a38b).

The key Kustomize idea:

\`\`\`yaml
images:
  - name: gitops-flask
    newName: <aws-account-id>.dkr.ecr.us-east-1.amazonaws.com/gitops-flask-app
    newTag: 1eda2123ef3b57054ac444f4842f60438e5d5571
\`\`\`

This is a **desired-state update**, not a call to Kubernetes. Argo CD later reads the merged Git state and issues Kubernetes changes. The distinction is why the pipeline is described as GitOps rather than a direct-action CD script.

Relevant workflow evidence:

- [GitHub Actions run #22](https://github.com/HafizMohammadSunasara/aws-eks-argocd-gitops/actions/runs/43748702205)
- [GitHub Actions run #23](https://github.com/HafizMohammadSunasara/aws-eks-argocd-gitops/actions/runs/43748769127)
- [Merged promotion PR #3](https://github.com/HafizMohammadSunasara/aws-eks-argocd-gitops/pull/3)

## 06 — Argo CD: the controller that closes the loop

An Argo CD Application defines:

- a repository URL,
- a Git target revision (\`main\`),
- a manifest path (\`k8s/overlays/dev\`),
- the Kubernetes API destination,
- and a namespace (\`gitops-demo\`).

In the initial setup, the application appeared **OutOfSync / Missing**. The observed commands then requested synchronization, and subsequent output showed **Synced / Healthy**, two ready Pods and a ClusterIP Service. Auto-sync was later reported enabled.

What do those statuses mean?

- **Synced:** the application resources match the desired Git revision as Argo CD evaluates them.
- **Healthy:** resource-level health checks, including the Kubernetes Deployment's available replica state, are satisfied.
- **OutOfSync:** desired and live states differ.
- **Missing:** a desired object is not present yet.

Synced/Healthy gives a strong deployment signal but doesn't prove load testing, failover, TLS, security review or externally accessible DNS.

### Kubernetes rolling update

Changing the image in the Deployment Pod template creates a new ReplicaSet. The controller scales new Pods while respecting the rollout strategy, then old Pods are retired. The Argo CD tree capture shows the Deployment, Service, older/newer ReplicaSets and healthy Pods. The successful \`kubectl rollout status\` message is an additional signal that the rollout finished.

The Version 2 screenshot showed a new Pod name, proving the displayed UI changed with a new workload instance. Pod names are ephemeral and **must not** be presented as stable URLs or immutable releases.

## 07 — Validation at three layers

**Layer A — Source/CI**

- Unit tests and validation completed successfully on the relevant workflow run.
- The workflow built the Docker image and published the SHA-tagged variant through its eligible path.

**Layer B — Desired/current cluster state**

- EKS cluster Active, two nodes Ready.
- \`gitops-flask-dev\` application Synced/Healthy.
- Flask Deployment 2/2 and Pods 1/1 Running in captured checks.
- New image tag in Kubernetes matched the promoted SHA in Git.

**Layer C — Application behavior**

- \`/healthz\` → HTTP 200, \`{"status":"ok"}\`
- \`/readyz\` → HTTP 200, \`{"status":"ready"}\`
- The browser at \`http://localhost:18081\` rendered the updated Version 2 heading.

These three layers together are stronger evidence than a single green badge.

### Repeatable checks (on an authorized workstation)

\`\`\`powershell
aws sts get-caller-identity
aws eks update-kubeconfig --region us-east-1 --name gitops-eks-cluster
kubectl get nodes -o wide
kubectl get applications -n argocd
kubectl get deployment,service,pods -n gitops-demo
kubectl rollout status deployment/gitops-flask -n gitops-demo --timeout=180s
\`\`\`

In **a separate PowerShell tab**, hold open:

\`\`\`powershell
kubectl -n gitops-demo port-forward --address 127.0.0.1 svc/gitops-flask 18081:80
\`\`\`

Then open \`http://127.0.0.1:18081\`. The port-forward process must remain running while browsing. The local URL works **only** on the machine hosting that port-forward. The IAM identity must be granted appropriate Kubernetes permissions; a valid AWS login alone does not guarantee access to every namespace.

## 08 — Debugging: real friction, accountable evidence

### Incident A — Argo CD initially OutOfSync / Missing

- **Observed:** Application was created, then reported \`OutOfSync\` and \`Missing\`.
- **Action captured:** A sync operation was requested and status was inspected again.
- **Result:** \`Synced\`, \`Healthy\`, two Pods ready, Service present.
- **Evidence:** [Initial state](evidence/screenshots/04-initial-sync-recovery.png), [health checks](evidence/screenshots/05-health-ready-checks.png).
- **What we cannot assert:** The screenshots alone do not prove every internal reconciliation decision.

### Incident B — Failed workflow followed by green runs

- **Observed:** Run #19 had a red failure indicator.
- **Follow-up:** Subsequent runs, including #20/#21 and the final #22/#23 demonstration, succeeded.
- **Evidence:** [History](evidence/screenshots/06-historical-ci-failure.png), [green run](evidence/screenshots/07-ci-green-after-fix.png).
- **Honesty:** An exact root-cause analysis requires the failed job's logs. A green subsequent run is not enough to invent the failing stack trace.

### Incident C — Windows localhost port 8080 unavailable

- **Observed:** \`kubectl port-forward ... 8080:443\` failed with a Windows bind/permissions error.
- **Change:** Forwarded Argo CD through the alternate local port \`18080\`.
- **Result:** Connection forwarding succeeded; the Argo UI loaded at \`https://localhost:18080\`.
- **Evidence:** [Error](evidence/screenshots/11-windows-port-8080-error.png), [working forward](evidence/screenshots/12-alternative-port-forward-working.png).

### Incident D — Kubernetes RBAC denied a Service read

- **Observed in a separate terminal screenshot:** an AWS IAM identity was forbidden from reading \`services\` in namespace \`gitops-demo\`.
- **Interpretation:** Authentication and authorization are different; Kubernetes RBAC/EKS access policy must grant the exact action.
- **Publication choice:** The original screenshot also displayed an Argo admin password. It was **not** included in the portfolio evidence.
- **Safe response:** Review EKS access entries or Kubernetes Role/RoleBinding scope and apply least privilege, rather than disabling authorization. Later successful access is demonstrated in the browser, but that by itself does not establish the precise access grant used.

## 09 — Security and what remains open

Controls present in source:

- OIDC-based AWS action in CI (no long-lived AWS access keys committed to the workflow).
- GitHub PR promotion instead of direct cluster deployment.
- Non-root container, read-only root, capability drops and bounded resource requests/limits.
- Separate internal ClusterIP Service and health endpoints.

Not fully established:

- End-to-end TLS/DNS/public ingress.
- Enforceable multi-AZ Pod placement and tested worker failure behavior.
- Image signature/digest attestation or complete SCA/SAST evidence.
- NetworkPolicy, WAF and comprehensive monitoring/alerting.
- Production-grade role review and credential-rotation verification.
- A successfully executed rollback and drift self-healing test.

Previous screenshots unintentionally exposed a long-lived AWS access key and Argo CD initial password. They are excluded; **assume compromised until rotated/revoked and the affected access is audited**. No credentials are packaged here.

## 10 — Rollback reasoning (procedure, not claimed demonstration)

The GitOps-safe idea is to change Git's desired image back to an earlier tested SHA, review/merge that change, and let Argo CD reconcile it. This creates an auditable history; it is different from issuing ad hoc \`kubectl set image\` in the cluster.

Suggested controlled lab exercise:

1. Record current image digest and Git revision.
2. Select a previously verified image SHA from ECR.
3. Open a PR that changes only the image tag in the Kustomize overlay.
4. Validate tests and policy; merge.
5. Observe Argo's sync history, Deployment rollout and HTTP response.
6. Document the exact old/new SHAs and recovery time.

**Status:** Pending demonstration, not counted as achieved.

## 11 — Cost, reproducibility and teardown

EKS control planes, EC2 workers, EBS volumes, NAT gateways, load balancers and container storage can continue billing when the browser is closed. A **running cluster screenshot is not a cost shutdown confirmation**.

For a new reader, the safest starting point is the tests and local Flask/Docker runtime in the original repository. Creating cloud resources requires an AWS account, applicable IAM permissions, budgets, and an explicit cleanup plan. Never paste keys into terminal screenshots, README text or repository issues.

The source snapshot under \`reference-source/\` is provided so the architecture is inspectable even if the original app changes in the future. The **authoritative live project** remains the original repository.

## 12 — What this project actually taught me

1. **A CI green check does not guarantee a running app.** You must verify registry, Git desired state, controller sync, Pod readiness and HTTP behavior.
2. **GitOps makes promotion reviewable.** The PR is the interface between build success and deployment intent.
3. **Controllers are eventually consistent.** Transitional OutOfSync/Missing states should be investigated, not hidden.
4. **Cloud IAM and Kubernetes RBAC are different authorization layers.**
5. **Local access and public hosting are different product states.**
6. **Evidence quality matters.** A before/after screenshot tied to a commit and a merged PR says more than an unqualified "production ready" badge.

---

### Navigation

[Portfolio home](README.md) · [Architecture](docs/02-architecture.md) · [Troubleshooting](docs/06-troubleshooting.md) · [Evidence index](evidence/INDEX.md) · [Roadmap](docs/12-roadmap.md)
