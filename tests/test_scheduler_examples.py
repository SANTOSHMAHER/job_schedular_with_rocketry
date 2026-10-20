import unittest

from app.scheduler_examples.apscheduler_app import (
    INTERVAL_SECONDS as APSCHEDULER_INTERVAL_SECONDS,
    create_scheduler,
)
from app.scheduler_examples.celery_app import (
    INTERVAL_SECONDS as CELERY_INTERVAL_SECONDS,
    celery_app,
    collect_live_data,
)


class SchedulerExampleTests(unittest.IsolatedAsyncioTestCase):
    def test_both_examples_use_the_same_two_minute_interval(self):
        self.assertEqual(APSCHEDULER_INTERVAL_SECONDS, 120)
        self.assertEqual(CELERY_INTERVAL_SECONDS, 120)

    async def test_apscheduler_registers_single_interval_job(self):
        scheduler = create_scheduler("https://example.test/data")
        scheduler.start()
        try:
            jobs = scheduler.get_jobs()

            self.assertEqual(len(jobs), 1)
            self.assertEqual(jobs[0].id, "collect_live_data")
            self.assertEqual(jobs[0].trigger.interval.total_seconds(), 120)
        finally:
            scheduler.shutdown(wait=False)

    def test_celery_beat_registers_collector_task(self):
        schedule = celery_app.conf.beat_schedule[
            "collect-live-data-every-two-minutes"
        ]

        self.assertEqual(schedule["task"], collect_live_data.name)
        self.assertEqual(schedule["schedule"], 120)
        self.assertIn(collect_live_data.name, celery_app.tasks)


if __name__ == "__main__":
    unittest.main()
