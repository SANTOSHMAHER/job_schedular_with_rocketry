# Demo: Rocketry with FastAPI (and React)

This is a demo for creating a scheduler with an API.
We use [Rocketry](https://rocketry.readthedocs.io/)
for our scheduler and [FastAPI](https://fastapi.tiangolo.com/)
for our API.

Key source files:

- ``app/api.py``: FastAPI application
- ``app/scheduler.py``: Rocketry application
- ``app/live_collector.py``: Optional scheduled HTTP JSON collector with SQLite storage
- ``app/main.py``: Main launch script

Add your tasks need to ``app/scheduler.py`` and 
modify ``app/api.py`` as needed.

## Installation

Clone this repository:

```console
git clone https://github.com/Miksus/rocketry-with-fastapi.git
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