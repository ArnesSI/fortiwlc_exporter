# FortiWLC Prometheus exporter

This project collects data from FortiNET WLC systems and generates export data
for Prometheus.

## Installing

TODO

## Running

FortiWLC exporter needs a configuration file to run. The format is an ini file
with a `main` section and a section for each WLC instance to monitor. The name
of those sections should match the name of the WLC instance.

Parameters for `main` section:

* `port` - TCP port for collector to listen on (default: 9118)
* `workers` - Number of WLC instances to poll at the same time (default: 2)
* `debug` - Run server in debug mode (default: "no")
* `username` & `password` - If you want to use the same username for all WLC instances, specify them in `main` section. Specifying `api_key` or `username` and `password` on WLC instance will override global setting for that instance.

WLC instance section parameters:

* `api_key` - REST API key to use when gathering data from this WLC
* `username` & `password` - If not using API keys specify username and password to login with

Example:

```ini
[main]
port = 9118

[mywlc]
api_key = "abc123456789"
```

When starting FortiWLC exporter, specify path to the configuration file with
`-c`. By default it will try to use `fortiwlc_exporter.ini` in the current directory.


## Description

TODO

## Developing

We use [poetry](https://poetry.eustace.io/) to manage Python dependencies and virtual environments.

To setup development virtual environment:

```
poetry install
```

There are also flake8 for linting, black for code formatting, pytest as a
test runner and coverage for unit test coverage. Write docstrings in google
style and check them via pydocstyle.

See documentation of your IDE on how to integrate these tools into your workflow. Here is how to run them manually via CLI:

```
poetry run flake8
poetry run black --diff --check .
poetry run pydocstyle fortiwlc_exporter
poetry run pytest --cov=fortiwlc_exporter tests
```

See Tests chapter below for more on running tests and code coverage.

Start exporter:

```
poetry run fortiwlc_exporter/exporter.py
```

### Tests

Unit tests with coverage in HTML:

```
poetry run pytest --cov=fortiwlc_exporter tests/unit
poetry run coverage html
```

Open [htmlcov/index.html](htmlcov/index.html) in your web browser.

### Releases

```
poetry run bumpversion patch
```

Instead of patch you can give `minor` or `major`.
This creates a commit and tag. Make sure to push it with `git push --tags`.

The `dev-version.sh` script will bump the version for development or release as
needed (based on whether we are on a git tag or not) and is called in CI jobs.
