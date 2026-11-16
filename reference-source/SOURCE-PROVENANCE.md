# Deployable source snapshot — provenance

This directory contains the application source and original GitOps manifests fetched from:

**https://github.com/HafizMohammadSunasara/aws-eks-argocd-gitops**

Pinned Git commit:

\`fd9714f7208c351340a471250dca940e90f2a38b\`

The archived source files here were retrieved from the source repository at that commit and their Git blob hashes were checked against GitHub.

## Deliberate exclusions

- The original repository's stale \`README.md\`, which still called AWS deployment pending despite later verified runtime evidence. The up-to-date portfolio README and \`DEEP-DIVE.md\` replace it in this presentation repository.
- The original \`assets/architecture.svg\`, whose design included optional/public networking as if part of the main path. The new \`../assets/architecture.svg\` distinguishes observed internal ClusterIP access from optional public ingress.
- The original 2-byte \`architecture.png\` placeholder.
- Original \`LICENSE\` duplicated at the portfolio root; the project is MIT-licensed.

The \`reference-source/.github/workflows/pipeline.yml\` file is nested under \`reference-source/\`. **It is a readable snapshot, not an active GitHub Actions workflow for this portfolio repo.** The deployable CI workflow is active only in the original application repository.

Do not change this snapshot to drive cloud deployment. Open changes against the original application repo instead.
