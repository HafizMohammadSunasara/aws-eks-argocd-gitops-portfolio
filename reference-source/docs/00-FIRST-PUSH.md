# First upload: exactly what to put on GitHub

Repository: **https://github.com/HafizMohammadSunasara/aws-eks-argocd-gitops**

## First, unzip the download

1. Download `aws-eks-argocd-gitops-starter.zip`.
2. Right-click → **Extract All** on Windows.
3. Open the extracted `aws-eks-argocd-gitops-starter` folder.
4. Upload its **contents** to the root of the GitHub repository. Do **not** upload the ZIP file as a single item; do **not** place everything under an extra `aws-eks-argocd-gitops-starter/` folder in GitHub.

The GitHub repository root must contain: `README.md`, `Dockerfile`, `requirements.txt`, `.github/`, `app/`, `tests/`, `k8s/`, `argocd/`, `scripts/`, `docs/`, `assets/`, etc.

## Option A: GitHub website (quickest for an empty repository)

1. Open the repository link above. Screenshot shows a new empty public repository.
2. Click **uploading an existing file** (or **Add file → Upload files**).
3. Drag/drop all extracted repository files and folders, including `.github` and the dotfiles (`.gitignore`, `.dockerignore`).
4. Carefully check the upload preview: nested folder paths must be preserved; do not flatten the directories.
5. Commit message: `feat: bootstrap GitOps EKS application and CI pipeline`.
6. Commit directly to `main` for this initial upload.
7. Return to the root and confirm that `README.md` renders the architecture and that **Actions** shows the first CI run.

**If the web uploader refuses a folder or misses dotfiles, use Option B.** Do not upload only the first-level files.

## Option B: GitHub Desktop or Git (more reliable for nested files)

1. In GitHub Desktop: **File → Clone repository**, select `HafizMohammadSunasara/aws-eks-argocd-gitops`, choose a local folder, then Clone.
2. Copy **the contents** of the extracted starter into the cloned repository folder; merge, do not move its `.git` folder.
3. In GitHub Desktop, verify the file changes; commit with message above, then **Push origin**.

Or using Git in a shell (in a directory where no same-named folder already exists):

```bash
git clone https://github.com/HafizMohammadSunasara/aws-eks-argocd-gitops.git
cd aws-eks-argocd-gitops
# Copy extracted starter files and directories here using File Explorer.
git add .
git status
git commit -m "feat: bootstrap GitOps EKS application and CI pipeline"
git push -u origin main
```

## First-upload verification gate

- [ ] `app/`, `k8s/`, `argocd/`, `assets/`, `docs/`, `tests/`, `scripts/` visible
- [ ] `.github/workflows/pipeline.yml` exists (in GitHub click `Go to file` to search)
- [ ] README shows an architecture graphic at the top
- [ ] GitHub Actions **test** job turns green
- [ ] Publish job is **skipped** because AWS variables are not configured yet
- [ ] No keys, passwords, kubeconfig or AWS tokens committed

**Stop here and send the repository screenshot or URL** before configuring AWS. A green CI job is not yet proof that EKS or the website exists.
