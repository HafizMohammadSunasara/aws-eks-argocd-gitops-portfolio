# Publishing the portfolio into a new GitHub repository

## Separation by design

- **Original application (leave untouched):** https://github.com/HafizMohammadSunasara/aws-eks-argocd-gitops
- **New portfolio repo (suggested name):** \`aws-eks-argocd-gitops-portfolio\`
- **Source snapshot:** \`reference-source/\`, commit \`fd9714f7208c351340a471250dca940e90f2a38b\`

This ZIP is intended to become the content of a **new repository**, not an upload into the existing application's \`main\` branch.

## Browser-upload route

1. Extract the downloaded ZIP to a local folder.
2. Create a new public GitHub repository with the name above; **do not** initialize with a different README if you plan to upload all provided files.
3. Upload the extracted folder's contents via GitHub **Add file → Upload files**. GitHub does **not** extract a ZIP as repository folders.
4. Make sure \`README.md\`, \`DEEP-DIVE.md\`, \`docs/\`, \`assets/\`, \`evidence/\`, and \`reference-source/\` appear at the **repository root**.
5. Commit changes. Inspect the README hero, architecture and screenshot links.

**Important:** Browser upload may not reliably include hidden files/folders such as \`.gitignore\`. Git on the command line is the more reliable route for complete trees.

## Git command-line route (PowerShell)

\`\`\`powershell
cd "path\to\extracted\Hafiz-EKS-GitOps-Gold-Portfolio"
git init -b main
git add .
git status
git commit -m "docs: launch black-gold EKS GitOps portfolio"
git remote add origin https://github.com/HafizMohammadSunasara/aws-eks-argocd-gitops-portfolio.git
git push -u origin main
\`\`\`

The remote repository must already exist. Review \`git status\` and \`git diff --cached\` before the commit. **Never** push \`.env\`, kubeconfig or screenshot files containing credentials.

## Publish the static showcase on GitHub Pages

1. Open the **new portfolio repository → Settings → Pages**.
2. Choose **Deploy from a branch**.
3. Select **\`main\` / \`/docs\`** and save.
4. Pages discovers \`docs/index.html\`.
5. Once published, the likely URL is \`https://hafizmohammadsunasara.github.io/aws-eks-argocd-gitops-portfolio/\`.

This is a **predicted path**, not a claim it is already live. The site is intentionally static and reads its screenshots/assets from relative URLs. It does **not** proxy an EKS app, expose the Kubernetes API or consume AWS billing.

## Final verification checklist

- [ ] Original application repository unchanged.
- [ ] New repo owner and name correct.
- [ ] README SVG hero loads in GitHub.
- [ ] All 16 evidence files render.
- [ ] The \`DEEP-DIVE.md\` and documentation links work.
- [ ] There is no active root \`.github/workflows/pipeline.yml\` in the portfolio repo.
- [ ] Pages site opens on desktop and mobile.
- [ ] No secrets, personal credentials or local paths are published.
- [ ] EKS deployment is not falsely described as publicly reachable.
