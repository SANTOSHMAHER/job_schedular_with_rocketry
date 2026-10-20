import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app.live_collector import fetch_and_store, fetch_json, store_snapshot


class LiveCollectorTests(unittest.TestCase):
    def test_store_snapshot_creates_table_and_persists_json(self):
        with tempfile.TemporaryDirectory() as directory:
            database_path = Path(directory) / "collector.sqlite3"
            payload = {"items": [{"id": 1, "value": "hello"}]}

            store_snapshot(database_path, "https://example.test/data", payload)

            connection = sqlite3.connect(database_path)
            try:
                source_url, fetched_at, payload_json = connection.execute(
                    """
                    SELECT source_url, fetched_at, payload_json
                    FROM fetch_snapshots
                    """
                ).fetchone()
            finally:
                connection.close()

        self.assertEqual(source_url, "https://example.test/data")
        self.assertTrue(fetched_at.endswith("Z"))
        self.assertEqual(json.loads(payload_json), payload)

    def test_fetch_json_rejects_non_http_urls(self):
        with self.assertRaisesRegex(ValueError, "HTTP or HTTPS"):
            fetch_json("file:///etc/passwd")

    def test_fetch_and_store_saves_response(self):
        class Response:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def read(self):
                return b'{"status": "ok"}'

        with tempfile.TemporaryDirectory() as directory:
            database_path = Path(directory) / "collector.sqlite3"
            with patch("app.live_collector.urlopen", return_value=Response()):
                fetch_and_store("https://example.test/data", database_path)

            connection = sqlite3.connect(database_path)
            try:
                payload_json = connection.execute(
                    "SELECT payload_json FROM fetch_snapshots"
                ).fetchone()[0]
            finally:
                connection.close()

        self.assertEqual(json.loads(payload_json), {"status": "ok"})


if __name__ == "__main__":
    unittest.main()
