"""Lightweight static checks; does not require an AWS account or EKS cluster."""

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def load(relative_path):
    file_path = ROOT / relative_path
    return yaml.safe_load(file_path.read_text(encoding="utf-8"))


def main():
    dep = load("k8s/base/deployment.yaml")
    svc = load("k8s/base/service.yaml")
    base = load("k8s/base/kustomization.yaml")
    overlay = load("k8s/overlays/dev/kustomization.yaml")
    argocd = load("argocd/application-dev.yaml")
    public = load("k8s/optional/public-nlb-service.yaml")

    # Kubernetes deployment validation
    assert dep["kind"] == "Deployment"
    assert dep["spec"]["replicas"] == 2, "Two application pods are expected"

    pod_labels = dep["spec"]["template"]["metadata"]["labels"]

    assert svc["spec"]["selector"] == pod_labels, (
        "Service selector must match Pods"
    )

    # Kustomize validation
    assert set(base["resources"]) == {
        "deployment.yaml",
        "service.yaml",
    }

    assert overlay["resources"] == ["../../base"]
    assert overlay["namespace"] == "gitops-demo"
    assert len(overlay["images"]) == 1
    assert overlay["images"][0]["name"] == "gitops-flask"

    # Argo CD application validation
    spec = argocd["spec"]

    assert spec["source"]["path"] == "k8s/overlays/dev"

    assert spec["source"]["repoURL"].endswith(
        "/aws-eks-argocd-gitops.git"
    )

    assert spec["destination"]["namespace"] == "gitops-demo"

    # Automated GitOps synchronization validation
    sync_policy = spec["syncPolicy"]
    automated = sync_policy.get("automated")

    assert isinstance(automated, dict), (
        "Automated GitOps synchronization must be configured"
    )

    assert automated.get("enabled") is True, (
        "Automated synchronization must be enabled"
    )

    assert automated.get("selfHeal") is True, (
        "GitOps self-healing must be enabled"
    )

    assert automated.get("prune") is False, (
        "Automatic resource pruning must remain disabled"
    )

    assert "CreateNamespace=true" in sync_policy.get("syncOptions", []), (
        "Namespace creation must be enabled"
    )

    # Optional public NLB service validation
    assert public["spec"]["loadBalancerClass"] == "service.k8s.aws/nlb"

    assert public["spec"]["selector"] == pod_labels

    print("PASS: Kubernetes manifests validated")
    print("PASS: Two application replicas configured")
    print("PASS: Kubernetes service selectors validated")
    print("PASS: Kustomize configuration validated")
    print("PASS: Argo CD repository and paths validated")
    print("PASS: Automated GitOps synchronization enabled")
    print("PASS: Self-healing enabled")
    print("PASS: Automatic pruning safely disabled")
    print("PASS: All manifest validation checks passed")


if __name__ == "__main__":
    main()
