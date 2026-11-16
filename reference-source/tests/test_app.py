import unittest

from app import create_app


class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        self.client = create_app().test_client()

    def test_index_has_project_name(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Amazon EKS", response.data)

    def test_health(self):
        response = self.client.get("/healthz")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "ok"})

    def test_ready(self):
        response = self.client.get("/readyz")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "ready"})

    def test_version(self):
        response = self.client.get("/version")
        self.assertEqual(response.status_code, 200)
        self.assertIn("version", response.json)


if __name__ == "__main__":
    unittest.main()
