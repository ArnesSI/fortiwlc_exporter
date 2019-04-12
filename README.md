# FortiWLC Prometheus exporter

This project collects data from FortiNET WLC systems and generates export data
for Prometheus.

## Installing

The exporter is compiled with pyinstaller, packaged as RPM and published in Arnes
internal YUM repo. The package is called `fortiwlc-exporter`.

```
yum install fortiwlc-exporter
```

## Running

FortiWLC exporter can use a YAML configuration file to set some parameters:

* `debug`: debug mode (default `false`)
* `no_default_collectors`: disable process, gc and other default collectors (default `true`)
* `timeout`: Timeout in seconds to generate a reply (default `60`)
* `exporter_port`: TCP port exporter should listen on (default `9118`)
* `wlc_username` & `wlc_password`: If not using API keys specify username and password to login with
* `wlc_api_key`: REST API key to use when gathering data from this WLC
* `wlcs`: List of WLC names to gather statistics from
* `workers`: Number of WLC instances to poll at the same time (default: `1`)

Example:

```yaml
---
exporter_port: 9118
wlc_api_key: "abc123456789"
wlcs:
  - wlc1
  - wlc2
```

When starting FortiWLC exporter, specify path to the configuration file with
`-c`.

You can override some settings from via command line arguments. Run `fortiwlc_exporter -h` for details.

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
