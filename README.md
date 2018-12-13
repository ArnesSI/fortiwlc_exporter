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
* `debug` - Run server in debug mode (default: "no")

WLC instance section parameters:

* `api_key` - REST API key to use when gathering data from this WLC (required)

Example:

```ini
[main]
port = 9118

[mywlc]
api_key = "abc123456789"
```

When starting FortiWLC exporter, specify path to the configuration file with 
`-c`. By default it will try to use `fortiwlc.ini` in the current directory.


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
