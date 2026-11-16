import tempfile
import unittest
from pathlib import Path

from scripts.update_image import update_image


class ImageUpdateTests(unittest.TestCase):
    def test_update_image_replaces_both_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "kustomization.yaml"
            path.write_text("images:\n  - name: gitops-flask\n    newName: old\n    newTag: bootstrap\n", encoding="utf-8")
            tag = "a" * 40
            image = "123456789012.dkr.ecr.us-east-1.amazonaws.com/gitops-demo"
            update_image(path, image, tag)
            result = path.read_text(encoding="utf-8")
            self.assertIn(f"newName: {image}", result)
            self.assertIn(f"newTag: {tag}", result)

    def test_rejects_non_ecr_registry(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "kustomization.yaml"
            path.write_text("newName: old\nnewTag: bootstrap\n")
            with self.assertRaises(ValueError):
                update_image(path, "docker.io/suspicious", "a" * 40)


if __name__ == "__main__":
    unittest.main()
