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

The project uses `pipenv` for managing python virtual environments.

To setup development vrtual environment:

```
pipenv install --dev
```

Running tests:

```
pipenv run python setup.py test
```

Tests include flake8 checks by default.
