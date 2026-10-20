"""Fetch JSON from a configured HTTP endpoint and save snapshots to SQLite."""

import asyncio
import json
import os
import sqlite3
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from rocketry.conds import every


DEFAULT_DATABASE_PATH = Path(__file__).resolve().parent.parent / "collector.sqlite3"
FETCH_TIMEOUT_SECONDS = 20


def validate_source_url(url):
    parsed_url = urlparse(url)
    if parsed_url.scheme not in ("http", "https") or not parsed_url.netloc:
        raise ValueError("LIVE_DATA_URL must be an absolute HTTP or HTTPS URL")


def fetch_json(url):
    validate_source_url(url)
    request = Request(url, headers={"Accept": "application/json"})
    with urlopen(request, timeout=FETCH_TIMEOUT_SECONDS) as response:
        return json.loads(response.read().decode("utf-8"))


def store_snapshot(database_path, source_url, payload):
    database_path = Path(database_path)
    database_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(database_path, timeout=10)
    try:
        with connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS fetch_snapshots (
                    id INTEGER PRIMARY KEY,
                    source_url TEXT NOT NULL,
                    fetched_at TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                )
                """
            )
            connection.execute(
                """
                INSERT INTO fetch_snapshots (source_url, fetched_at, payload_json)
                VALUES (?, strftime('%Y-%m-%dT%H:%M:%fZ', 'now'), ?)
                """,
                (source_url, json.dumps(payload, ensure_ascii=False)),
            )
    finally:
        connection.close()


def fetch_and_store(source_url, database_path):
    payload = fetch_json(source_url)
    store_snapshot(database_path, source_url, payload)


def register_live_collector(rocketry_app):
    """Register the two-minute collector when LIVE_DATA_URL is configured."""
    source_url = os.environ.get("LIVE_DATA_URL")
    if not source_url:
        return False

    validate_source_url(source_url)
    database_path = Path(
        os.environ.get("LIVE_DATA_DB", str(DEFAULT_DATABASE_PATH))
    )

    @rocketry_app.task(every("2 minutes", based="finish"))
    async def collect_live_data():
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(
            None,
            fetch_and_store,
            source_url,
            database_path,
        )

    return True
