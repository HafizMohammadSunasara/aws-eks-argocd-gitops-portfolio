# Later phases: AWS, ECR, EKS and Argo CD setup

**This is a preparation checklist, not a record of completed AWS deployment.** Do not run everything in one go. Complete each verification gate first.

## Phase A — AWS identity and billing guardrails

1. Choose region `us-east-1`, and check you are in the intended AWS account.
2. Create AWS Budgets alerts and estimate EKS control-plane hours, two EC2 nodes, NAT Gateway, load balancer and public IPv4 charges.
3. Plan separate least-privilege roles for EKS control plane, EC2 worker nodes, GitHub Actions OIDC publishing, and AWS Load Balancer Controller.
4. Never create static AWS access keys for GitHub Actions.

## Phase B — New networking (standard EKS)

1. Create a new VPC (example `10.40.0.0/16`) in `us-east-1`.
2. Create public subnet A and public subnet B in **different Availability Zones**.
3. Create private subnet A and private subnet B in those same distinct AZs; ensure non-overlapping CIDRs.
4. Attach an Internet Gateway and a public route table (`0.0.0.0/0` via IGW) to both public subnets.
5. Provide outbound internet from private subnets, e.g., a NAT Gateway in one public subnet for a **cost-optimized lab only**. One NAT Gateway is not an HA production design.
6. Tag public subnets for public load balancer discovery and private subnets for internal load balancers, and verify EKS-specific subnet requirements.
7. Review security groups and network ACLs before creating nodes.

## Phase C — EKS + exactly 2 initial managed worker nodes

1. Create a **standard EKS cluster** (not EKS Auto Mode), select a currently supported Kubernetes release and a dedicated cluster IAM role.
2. Select the new VPC and at least two appropriate private subnets; review endpoint and log settings.
3. Wait until cluster status becomes `ACTIVE`.
4. Create a **managed node group** with the correct EKS node IAM role and private subnets in both AZs.
5. Start with **desired=2, min=2, max=3**; desired is the initial two-node count, max is a future scaling limit.
6. Configure authorized `kubectl` access and verify:

```bash
aws eks update-kubeconfig --region us-east-1 --name YOUR_CLUSTER_NAME
kubectl get nodes -o wide
kubectl get pods -n kube-system
```

**Gate:** 2 nodes `Ready` and EKS core add-ons healthy. If nodes fail, stop; do not add Argo CD yet.

## Phase D — ECR and GitHub OIDC

1. Create a private ECR repository, e.g. `gitops-argocd-eks-demo`, enable scanning and configure retention.
2. Create GitHub OIDC identity provider `token.actions.githubusercontent.com` if not present, then a narrowly scoped AWS role that can push to this one ECR repository.
3. Lock the role's OIDC trust to this repository and `main` branch, not wildcard GitHub users.
4. In **GitHub → Settings → Secrets and variables → Actions → Variables**, set:

| Variable | Example / purpose |
| --- | --- |
| `AWS_REGION` | `us-east-1` |
| `AWS_ROLE_ARN` | `arn:aws:iam::YOUR_ACCOUNT_ID:role/YOUR_GITHUB_OIDC_ECR_ROLE` |
| `ECR_REPOSITORY` | `gitops-argocd-eks-demo` |

The role ARN is an identifier, not a password. Never put AWS access keys in the repo. Restrict IAM permissions to the exact ECR repo where possible.

5. GitHub repository **Settings → Actions → General → Workflow permissions**: enable **Allow GitHub Actions to create and approve pull requests** *only if you intend the automated promotion PR to work*; this is required for the included PR-creation workflow and may be disabled by default.
6. Trigger a trusted source-code push to `main`. GitHub Actions should: test → build → OIDC → ECR push → open an image promotion PR. Review the ECR tag and PR diff.

**Gate:** ECR contains a real 40-character commit SHA tag; a PR updates `newName` and `newTag` in `k8s/overlays/dev/kustomization.yaml`.

## Phase E — Self-managed Argo CD on EKS

This training project uses **self-managed Argo CD inside EKS**. AWS also has an EKS Argo CD capability, but that is a different installation and IAM workflow. Do not mix them.

1. Confirm `kubectl` sees the intended cluster and exactly two healthy nodes.
2. Create the Argo CD namespace and install a **reviewed, supported pinned Argo CD release** using the [official install instructions](https://argo-cd.readthedocs.io/en/stable/getting_started/).
3. Verify Argo CD controller, repo server, application controller and API server Pods are Ready.
4. Use **port-forwarding** for first login; protect/rotate bootstrap admin credentials, do not expose the admin UI publicly.
5. Confirm the image-promotion PR has been reviewed and merged; do not sync the `000000000000` placeholder image.
6. Bootstrap the Application once:

```bash
kubectl apply -n argocd -f argocd/application-dev.yaml
kubectl get applications -n argocd
```

7. Open Argo CD UI, inspect diff/desired state, then perform the **first manual sync**.
8. Verify:

```bash
kubectl get deployment,replicaset,pods,service -n gitops-demo -o wide
kubectl rollout status deployment/gitops-flask -n gitops-demo
kubectl get pods -n gitops-demo -l app=gitops-flask
```

**Gate:** `Healthy` + `Synced`, two ready application Pods, private ClusterIP Service responds in a safe internal test.

## Phase F — Optional internet-facing NLB

1. First install/configure **AWS Load Balancer Controller** with the dedicated IAM role, and confirm it is healthy. Verify public subnet tagging and default routes to the Internet Gateway.
2. Commit the optional NLB Service into the dev overlay by adding the following resource to `k8s/overlays/dev/kustomization.yaml`:

```yaml
resources:
  - ../../base
  - ../../optional/public-nlb-service.yaml
```

3. Let Argo CD sync the change rather than manually applying the Service. Confirm the AWS NLB uses an **internet-facing** scheme.
4. Verify targets healthy, public DNS resolves and HTTP returns the Flask homepage. Do not call plain HTTP production-ready; add TLS/domain/access controls in a subsequent hardening phase.

## Phase G — Prove GitOps

1. Modify the visible application text, commit to a reviewed PR, merge to `main`.
2. CI builds and pushes a new SHA image, then proposes a new GitOps image-tag PR.
3. Merge the promotion PR; observe Argo CD's diff, reconciliation and rolling Deployment update.
4. After safe validation, enable automated sync/self-heal in `argocd/application-dev.yaml`:

```yaml
syncPolicy:
  automated:
    prune: false
    selfHeal: true
  syncOptions:
    - CreateNamespace=true
    - PruneLast=true
```

5. Demonstrate a controlled non-destructive config drift and its correction. Demonstrate a Git revert to a previous working image SHA and let Argo CD sync it.
6. Capture evidence, logs, and redacted screenshots for your portfolio.

## Official references

- [GitHub OIDC in AWS](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws)
- [Amazon EKS IAM and node groups](https://docs.aws.amazon.com/eks/latest/userguide/managed-node-groups.html)
- [Argo CD Application specification](https://argo-cd.readthedocs.io/en/stable/user-guide/application-specification/)
- [AWS Load Balancer Controller installation](https://docs.aws.amazon.com/eks/latest/userguide/lbc-manifest.html)
