# 04 — CI/CD: understand the conditions, not only the green checkmark

## Exact workflow

The original app uses [\`.github/workflows/pipeline.yml\`](../reference-source/.github/workflows/pipeline.yml). The job graph is:

1. \`test\` — unit tests, YAML checks, Docker build.
2. \`publish\` — only after \`test\`, only on qualifying \`push\` with required repository variables present.

### Event matrix

| Trigger | Test job | ECR publish job |
|---|---|---|
| Pull request into \`main\` | Runs | **Skipped by design** |
| Eligible push to \`main\` on watched code paths | Runs | Runs if vars are configured and tests pass |
| Manual workflow dispatch | Runs | Skipped by current \`push\` condition |

The \`push\` path filter watches app, tests, scripts, Dockerfile, requirements and the workflow file. A docs-only commit may not start the application workflow. This is intentional—documentation updates should not cause unnecessary ECR builds.

## Why the PR screenshot said 'This job was skipped'

[Screenshot 08](../evidence/screenshots/08-intentional-pr-publish-skip.png) shows the publish job skipped while PR validation completed. The workflow condition is the reason; skipped does not mean failed.

## Tests and gates

The Python test suite verifies routes and version behavior, while the manifest validation script enforces expected Kubernetes/Argo structure. A Docker build ensures the container recipe remains buildable. These checks reduce risk; they are not substitutes for vulnerability scanning, policy checks and running the built image.

Local verification, from the original app repository:

\`\`\`powershell
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python scripts/validate_manifests.py
docker build -t gitops-flask:local .
\`\`\`

## ECR publishing and OIDC

The publish job requests GitHub \`id-token: write\` and assumes an AWS role using \`aws-actions/configure-aws-credentials\`. Its Docker tag uses \`github.sha\`. The helper updates the Kustomize overlay and \`peter-evans/create-pull-request\` creates the promotion PR.

The workflow **does not call kubectl to deploy**. That is a deliberate separation of duties.

## Evidence

- [Historical red run](../evidence/screenshots/06-historical-ci-failure.png).
- [Later green workflow](../evidence/screenshots/07-ci-green-after-fix.png).
- [Run #22](https://github.com/HafizMohammadSunasara/aws-eks-argocd-gitops/actions/runs/43748702205).
- [Run #23](https://github.com/HafizMohammadSunasara/aws-eks-argocd-gitops/actions/runs/43748769127).
- [Promotion PR #3 merged](https://github.com/HafizMohammadSunasara/aws-eks-argocd-gitops/pull/3).

**Unverified detail:** The failed run's exact root cause is not derived from a red status icon alone. An incident report should quote the failing job logs before asserting why the failure happened.
