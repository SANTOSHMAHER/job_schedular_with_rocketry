"""Celery application and Beat schedule for the shared live-data collector."""

import os
from pathlib import Path

from celery import Celery

from app.live_collector import (
    DEFAULT_DATABASE_PATH,
    fetch_and_store,
)

INTERVAL_SECONDS = 120
BROKER_URL = os.environ.get(
    "CELERY_BROKER_URL",
    "redis://localhost:6379/0",
)

celery_app = Celery(
    "scheduler_comparison",
    broker=BROKER_URL,
)
celery_app.conf.update(
    enable_utc=True,
    timezone="UTC",
    beat_schedule={
        "collect-live-data-every-two-minutes": {
            "task": "app.scheduler_examples.celery_app.collect_live_data",
            "schedule": INTERVAL_SECONDS,
        }
    },
)


@celery_app.task(name="app.scheduler_examples.celery_app.collect_live_data")
def collect_live_data():
    source_url = os.environ.get("LIVE_DATA_URL")
    if not source_url:
        raise RuntimeError("Set LIVE_DATA_URL in the Celery worker environment")

    database_path = Path(
        os.environ.get("LIVE_DATA_DB", str(DEFAULT_DATABASE_PATH))
    )
    fetch_and_store(source_url, database_path)
