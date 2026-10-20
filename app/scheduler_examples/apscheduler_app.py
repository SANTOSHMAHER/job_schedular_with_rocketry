"""Run the shared live-data collector with APScheduler."""

import asyncio
import os
from pathlib import Path

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.live_collector import (
    DEFAULT_DATABASE_PATH,
    fetch_and_store,
    validate_source_url,
)

INTERVAL_SECONDS = 120


def create_scheduler(source_url, database_path=DEFAULT_DATABASE_PATH):
    validate_source_url(source_url)
    scheduler = AsyncIOScheduler(timezone="UTC")

    async def collect_live_data():
        await asyncio.to_thread(
            fetch_and_store,
            source_url,
            Path(database_path),
        )

    scheduler.add_job(
        collect_live_data,
        trigger="interval",
        seconds=INTERVAL_SECONDS,
        id="collect_live_data",
        max_instances=1,
        coalesce=True,
        replace_existing=True,
    )
    return scheduler


async def main():
    source_url = os.environ.get("LIVE_DATA_URL")
    if not source_url:
        raise RuntimeError("Set LIVE_DATA_URL before starting APScheduler")

    database_path = Path(
        os.environ.get("LIVE_DATA_DB", str(DEFAULT_DATABASE_PATH))
    )
    scheduler = create_scheduler(source_url, database_path)
    scheduler.start()
    try:
        await asyncio.Event().wait()
    finally:
        scheduler.shutdown(wait=False)


if __name__ == "__main__":
    asyncio.run(main())
