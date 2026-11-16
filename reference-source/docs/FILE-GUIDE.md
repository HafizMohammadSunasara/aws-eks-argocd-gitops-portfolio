# Which file does what? Beginner explanation

| File or folder | Plain-language role | When used |
| --- | --- | --- |
| `README.md` | Recruiter-friendly landing page, problem statement, architecture, honest status. | Immediately after pushing |
| `assets/architecture.svg` / `.png` | Actual visual workflow, used in README and presentations. | Immediately |
| `app/__init__.py` | Starts Flask and defines `/`, `/healthz`, `/readyz`, `/version`. | Local run and EKS runtime |
| `app/templates/index.html` | Pretty web page shown in browser. | HTTP requests |
| `app/static/style.css` | Colors, responsive layout and branding. | HTTP requests |
| `tests/test_app.py` | Checks that website and health endpoints respond correctly. | Every CI run |
| `tests/test_image_update.py` | Ensures image-tag updater accepts real ECR URI and rejects wrong registries. | Every CI run |
| `requirements.txt` | Runtime Python dependencies (Flask and Gunicorn). | Python install and Docker build |
| `requirements-dev.txt` | Runtime dependencies plus YAML checks. | CI and local tests |
| `Dockerfile` | Packages the Flask application as a non-root container listening on 8080. | Docker build and ECR push |
| `.dockerignore` | Removes unnecessary files from Docker build context. | Docker build |
| `.gitignore` | Prevents common secrets, local caches and state files entering Git. | Git add/commit |
| `.env.example` | Demonstrates optional local settings without actual secrets. | Local development |
| `.github/workflows/pipeline.yml` | Tests on PR/main; after AWS OIDC/ECR setup, publishes an image and creates a promotion PR. | GitHub Actions |
| `k8s/base/deployment.yaml` | Desired 2 app replicas, probes, resource settings and security. | Argo CD/Kubernetes |
| `k8s/base/service.yaml` | Stable private address directing traffic to Pods. | Kubernetes |
| `k8s/base/kustomization.yaml` | Collects Deployment and Service as reusable base. | Kustomize build |
| `k8s/overlays/dev/kustomization.yaml` | Sets dev namespace and **exact ECR image + immutable SHA tag**. | Argo CD source of truth |
| `k8s/optional/public-nlb-service.yaml` | Optional AWS Load Balancer Controller NLB; do not apply until controller/subnets are ready. | Final public access phase |
| `argocd/application-dev.yaml` | Tells Argo CD which Git branch/path to watch and which namespace to target. | Argo CD installation phase |
| `scripts/update_image.py` | Safely updates only the ECR image and SHA in the dev overlay. | CI publish job |
| `scripts/validate_manifests.py` | Checks YAML structure and important references before cloud deployment. | Every CI run |
| `docs/00-FIRST-PUSH.md` | Upload instructions and first verification gate. | Right now |
| `docs/AWS-AND-ARGOCD-SETUP.md` | AWS roles, VPC/EKS, OIDC/ECR and Argo CD follow-up sequence. | After first green CI |
| `docs/TROUBLESHOOTING.md` | Errors to recognize and diagnostic commands. | When blocked |
| `docs/COST-AND-CLEANUP.md` | Charges, cleanup order, and how to avoid resource leaks. | Before AWS and at finish |
| `LICENSE` | Permission and reuse conditions (MIT). | Public GitHub |

## Four concepts beginners confuse

1. **EKS cluster vs 2 worker nodes:** the cluster is Kubernetes control plane; EC2 worker nodes run the Pods. Two nodes is not the same thing as two Pods, even though this lab starts with both counts equal to two.
2. **Docker image vs GitOps manifest:** ECR stores the binary image; Git stores the desired version and Kubernetes configuration.
3. **CI vs Argo CD:** GitHub Actions never needs deployment access to the EKS API in this design. Argo CD deploys after reading Git.
4. **Private Service vs public NLB:** The first ClusterIP Service is intentionally only inside the cluster. Public internet access is added later using a properly configured AWS Load Balancer Controller and NLB.
