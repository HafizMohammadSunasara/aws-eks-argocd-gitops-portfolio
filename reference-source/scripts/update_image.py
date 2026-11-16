"""Replace the dev Kustomize image with an ECR URI and immutable commit SHA.

Uses only Python's standard library, so GitHub Actions needs no extra YAML tool.
"""

import argparse
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FILE = ROOT / "k8s" / "overlays" / "dev" / "kustomization.yaml"
IMAGE_RE = re.compile(r"^\d{12}\.dkr\.ecr\.[a-z0-9-]+\.amazonaws\.com/[a-zA-Z0-9._/-]+$")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def update_image(path: Path, image: str, tag: str) -> None:
    if not IMAGE_RE.fullmatch(image):
        raise ValueError("Expected a private ECR image URI such as 123456789012.dkr.ecr.us-east-1.amazonaws.com/my-repo")
    if not SHA_RE.fullmatch(tag):
        raise ValueError("Image tag must be a full 40-character lowercase Git commit SHA")

    original = path.read_text(encoding="utf-8")
    updated, count_name = re.subn(
        r"(?m)^(\s*newName:\s*)[^\n#]+$", lambda m: m.group(1) + image, original
    )
    updated, count_tag = re.subn(
        r"(?m)^(\s*newTag:\s*)[^\n#]+$", lambda m: m.group(1) + tag, updated
    )
    if count_name != 1 or count_tag != 1:
        raise ValueError("Expected exactly one newName and one newTag in the dev Kustomization")
    path.write_text(updated, encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", required=True, help="ECR repository URI WITHOUT tag")
    parser.add_argument("--tag", required=True, help="Full 40-character commit SHA")
    parser.add_argument("--file", type=Path, default=DEFAULT_FILE)
    args = parser.parse_args()
    update_image(args.file, args.image, args.tag)
    print(f"Updated {args.file} to {args.image}:{args.tag}")
