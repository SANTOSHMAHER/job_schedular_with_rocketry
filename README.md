# Scheduler comparison with FastAPI

This project compares [Rocketry](https://rocketry.readthedocs.io/),
[APScheduler](https://apscheduler.readthedocs.io/), and
[Celery Beat](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html)
using the same scheduled JSON collector. The original Rocketry and FastAPI demo
code is retained with its existing license and author attribution.

Key source files:

- ``app/api.py``: FastAPI application
- ``app/scheduler.py``: Rocketry application
- ``app/live_collector.py``: Optional scheduled HTTP JSON collector with SQLite storage
- ``app/scheduler_examples/``: Optional APScheduler and Celery Beat comparison examples
- ``app/main.py``: Main launch script

Add your tasks need to ``app/scheduler.py`` and 
modify ``app/api.py`` as needed.

## Installation

Clone this repository:

```console
git clone https://github.com/SANTOSHMAHER/job_schedular_with_rocketry.git
```

Make sure you have Python 3.7 or newer.
Then just install the dependencies:

```console
pip install -r requirements.txt
```

## Running

To enable the sample collector, configure an HTTP or HTTPS JSON endpoint before
starting the app. It saves each response as a JSON snapshot in
``collector.sqlite3`` in the repository root. The collector is disabled when
``LIVE_DATA_URL`` is not set.

PowerShell:

```powershell
$env:LIVE_DATA_URL = "https://your-service.example/api/data"
python app\main.py
```

The collector runs every two minutes, measured from the end of the previous
run. Set ``LIVE_DATA_DB`` to choose a different SQLite file. The endpoint and
database path are read at startup; restart the app to apply changes. Each
snapshot is stored in the ``fetch_snapshots`` table with its source URL,
fetch time, and JSON payload. API-controlled schedule changes are not
implemented yet.

### Comparing APScheduler and Celery Beat

The optional examples use the same HTTP JSON collector and SQLite table as the
Rocketry example. They each run every 120 seconds. Run only one scheduler at a
time to avoid duplicate fetches. These examples are separate from the FastAPI
application and do not replace Rocketry.

Install the comparison dependencies into the active Python environment:

```powershell
python -m pip install -r requirements-comparison.txt
```

Set the endpoint for each example:

```powershell
$env:LIVE_DATA_URL = "https://your-service.example/api/data"
```

Run APScheduler:

```powershell
python -m app.scheduler_examples.apscheduler_app
```

Celery Beat needs a running Redis broker. The default broker is
``redis://localhost:6379/0``; set ``CELERY_BROKER_URL`` to override it. If
Docker is installed, start Redis in a separate terminal:

```powershell
docker run --name scheduler-redis -p 6379:6379 -d redis:7-alpine
```

In one terminal, start the Celery worker:

```powershell
celery -A app.scheduler_examples.celery_app:celery_app worker --pool=solo --loglevel=INFO
```

In another terminal, start Celery Beat:

```powershell
celery -A app.scheduler_examples.celery_app:celery_app beat --loglevel=INFO
```

Set ``LIVE_DATA_URL`` (and optionally ``LIVE_DATA_DB``) in both Celery
terminals. Celery Beat sends scheduled work to the worker through Redis; it
does not execute the collector itself. On Windows, ``--pool=solo`` avoids
Celery's unsupported prefork worker pool.

If the collector is not needed, start the app without setting ``LIVE_DATA_URL``:

```console
python app/main.py
```

## Front-end

For the front-end, download [Node](https://nodejs.org/en/), [npm](https://www.npmjs.com/) and [yarn](https://classic.yarnpkg.com).
Then change to frontend directory to install the Node modules:

```npm
yarn install
```

Then start the server:

```npm
yarn start
```

![UI example](https://github.com/Miksus/rocketry-with-fastapi/blob/master/docs/demo.gif)

## What next?

Read more about Rocketry:

- Documentation: https://rocketry.readthedocs.io/
- Source code: https://github.com/Miksus/rocketry

Read more about FastAPI:

- Documentation: https://fastapi.tiangolo.com/
- Source code: https://github.com/tiangolo/fastapi

Read more about React:

- Documentation: https://reactjs.org/
- Source code: https://github.com/facebook/react


Author: [Mikael Koli](https://github.com/Miksus)