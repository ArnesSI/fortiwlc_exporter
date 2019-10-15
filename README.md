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

Example:

```yaml
---
exporter_port: 9118
wlc_api_key: "abc123456789"
```

When starting FortiWLC exporter, specify path to the configuration file with
`-c`.

You can override some settings from via command line arguments. Run `fortiwlc_exporter -h` for details.

## Description

To scrape stats for a given WLC open URL: [http://[exporter]:[port]/probe?target=[wlc_name]](http://[exporter]:[port]/probe?target=[wlc_name])

Exporter returns these metrics:

1. **`fortiwlc_clients`**  
   Number of clients connected to a specific combination of access point, radio and wifi network in a campus. Labels:
   * `ap_name`: Name of access point
   * `radio_type`: Radio standard. Common values are: `802.11ac`, `802.11g`, `802.11n`, `802.11n-5G`, `unknown` It is unlikely, but additional values could occur
   * `wifi_network`: Name of wireless network. Commonly build from campus_id and SSID
   * `campus`: Campus slug of AP. Can be missing.
2. **`fortiwlc_wifi_info`**  
   Wireless network (SSID) information. This is an info metric, so tis values is always 1. Labels:
   * `wifi_network`: Name of wireless network. Commonly build from campus_id and SSID. Guarantied to be unique
   * `ssid`: Advertised SSID of wireless network
3. **`fortiwlc_ap_info`**  
   Access point information. This is an info metric, so tis values is always 1. Labels:
   * `ap_name`: Name of access point
   * `wlc`: Hostname of wireless controller managing this access point
   * `ap_status`: Connection status. Common values: `connected`, `disconnected`, `connecting`
   * `ap_state`: Authorization state. Common values: `authorized`, `discovered`
   * `os_version`: Version of firmware running on access point. Can be `unknown`
   * `serial_number`: Access point's serial number. Can be `unknown`
   * `profile`: Name of AP profile.
   * `model`: Model of AP.
   * `campus`: Campus slug. Derived from `profile`. Can be missing.
4. **`fortiwlc_up`**  
   Was the last scrape of data from FortiNET WLC instance successful. Labels:
   * `wlc`: Hostname of wireless controller queried
5. **`fortiwlc_receive_bytes_total`**  
   Total of received bytes. Labels:
   * `wlc`: Hostname of wireless controller queried
   * `ap_name`: Name of access point
   * `interface`: Name of interface
   * `campus`: Campus slug. Derived from `profile`. Can be missing.
6. **`fortiwlc_transmit_bytes_total`**  
   Total of transmitted bytes. Labels:
   * `wlc`: Hostname of wireless controller queried
   * `ap_name`: Name of access point
   * `interface`: Name of interface
   * `campus`: Campus slug. Derived from `profile`. Can be missing.
7. **`fortiwlc_receive_packets_total`**  
   Total of received packets. Labels:
   * `wlc`: Hostname of wireless controller queried
   * `ap_name`: Name of access point
   * `interface`: Name of interface
   * `campus`: Campus slug. Derived from `profile`. Can be missing.
8. **`fortiwlc_transmit_packets_total`**  
   Total of transmitted packets. Labels:
   * `wlc`: Hostname of wireless controller queried
   * `ap_name`: Name of access point
   * `interface`: Name of interface
   * `campus`: Campus slug. Derived from `profile`. Can be missing.
9. **`fortiwlc_receive_errs_total`**  
   Total of received errors. Labels:
   * `wlc`: Hostname of wireless controller queried
   * `ap_name`: Name of access point
   * `interface`: Name of interface
   * `campus`: Campus slug. Derived from `profile`. Can be missing.
10. **`fortiwlc_transmit_errs_total`**  
   Total of transmitted errors. Labels:
   * `wlc`: Hostname of wireless controller queried
   * `ap_name`: Name of access point
   * `interface`: Name of interface
   * `campus`: Campus slug. Derived from `profile`. Can be missing.
11. **`fortiwlc_receive_drop_total`**  
   Total of received drops. Labels:
   * `wlc`: Hostname of wireless controller queried
   * `ap_name`: Name of access point
   * `interface`: Name of interface
   * `campus`: Campus slug. Derived from `profile`. Can be missing.
12. **`fortiwlc_transmit_drop_total`**  
   Total of transmitted drops. Labels:
   * `wlc`: Hostname of wireless controller queried
   * `ap_name`: Name of access point
   * `interface`: Name of interface
   * `campus`: Campus slug. Derived from `profile`. Can be missing.
13. **`fortiwlc_transmit_colls_total`**  
   Total of transmitted collisions. Labels:
   * `wlc`: Hostname of wireless controller queried
   * `ap_name`: Name of access point
   * `interface`: Name of interface
   * `campus`: Campus slug. Derived from `profile`. Can be missing.

Sample response:

```
# HELP fortiwlc_clients Number of clients connected to a specific combination of access point, radio and wifi network in a campus.
# TYPE fortiwlc_clients gauge
fortiwlc_clients{ap_name="w1-tolos.cpe.arnes.si",campus="tolos",radio_type="802.11ac",wifi_network="1_tolos_psk"} 1.0
fortiwlc_clients{ap_name="w1-tolos.cpe.arnes.si",campus="tolos",radio_type="802.11ac",wifi_network="1_eduroam"} 0.0
fortiwlc_clients{ap_name="w1-tolos.cpe.arnes.si",campus="tolos",radio_type="unknown",wifi_network="1_eduroam"} 0.0
fortiwlc_clients{ap_name="w1-tolos.cpe.arnes.si",campus="tolos",radio_type="802.11n",wifi_network="1_eduroam"} 0.0
fortiwlc_clients{ap_name="w1-tolos.cpe.arnes.si",campus="tolos",radio_type="802.11g",wifi_network="1_eduroam"} 0.0
fortiwlc_clients{ap_name="w1-tolos.cpe.arnes.si",campus="tolos",radio_type="802.11n-5G",wifi_network="1_eduroam"} 0.0
fortiwlc_clients{ap_name="w1-tolos.cpe.arnes.si",campus="tolos",radio_type="unknown",wifi_network="1_tolos_psk"} 0.0
fortiwlc_clients{ap_name="w1-tolos.cpe.arnes.si",campus="tolos",radio_type="802.11n",wifi_network="1_tolos_psk"} 0.0
fortiwlc_clients{ap_name="w1-tolos.cpe.arnes.si",campus="tolos",radio_type="802.11g",wifi_network="1_tolos_psk"} 0.0
fortiwlc_clients{ap_name="w1-tolos.cpe.arnes.si",campus="tolos",radio_type="802.11n-5G",wifi_network="1_tolos_psk"} 0.0
fortiwlc_clients{ap_name="w1-volantis.cpe.arnes.si",campus="volantis",radio_type="802.11ac",wifi_network="2_eduroam"} 0.0
fortiwlc_clients{ap_name="w1-volantis.cpe.arnes.si",campus="volantis",radio_type="unknown",wifi_network="2_eduroam"} 0.0
fortiwlc_clients{ap_name="w1-volantis.cpe.arnes.si",campus="volantis",radio_type="802.11n",wifi_network="2_eduroam"} 0.0
fortiwlc_clients{ap_name="w1-volantis.cpe.arnes.si",campus="volantis",radio_type="802.11g",wifi_network="2_eduroam"} 0.0
fortiwlc_clients{ap_name="w1-volantis.cpe.arnes.si",campus="volantis",radio_type="802.11n-5G",wifi_network="2_eduroam"} 0.0
# HELP fortiwlc_ap_info Access point information
# TYPE fortiwlc_ap_info gauge
fortiwlc_ap_info{ap_name="w1-tolos.cpe.arnes.si",ap_state="authorized",ap_status="connected",campus="tolos",model="FAP221E",os_version="v5.6-build6508",profile="tolos_FAP221E",wlc="wlc.ansoext.arnes.si"} 1.0
fortiwlc_ap_info{ap_name="w1-volantis.cpe.arnes.si",ap_state="authorized",ap_status="connected",campus="volantis",model="FAP221E",os_version="v6.0-build0057",profile="volantis_FAP221E",wlc="wlc.ansoext.arnes.si"} 1.0
# HELP fortiwlc_wifi_info Wireless network (SSID) information
# TYPE fortiwlc_wifi_info gauge
fortiwlc_wifi_info{ssid="tolos_psk",wifi_network="1_tolos_psk"} 1.0
fortiwlc_wifi_info{ssid="eduroam",wifi_network="1_eduroam"} 1.0
fortiwlc_wifi_info{ssid="eduroam",wifi_network="2_eduroam"} 1.0
# HELP fortiwlc_up Was the last scrape of data from FortiNET WLC instance successful.
# TYPE fortiwlc_up gauge
fortiwlc_up{wlc="wlc.ansoext.arnes.si"} 1.0
# HELP fortiwlc_receive_bytes_total Wired metrics
# TYPE fortiwlc_receive_bytes_total counter
fortiwlc_receive_bytes_total{ap_name="w1-tolos.cpe.arnes.si",campus="volantis",interface="eth0",wlc="wlc.ansoext.arnes.si"} 0.0
fortiwlc_receive_bytes_total{ap_name="w1-volantis.cpe.arnes.si",campus="volantis",interface="eth0",wlc="wlc.ansoext.arnes.si"} 0.0
# HELP fortiwlc_transmit_bytes_total Wired metrics
# TYPE fortiwlc_transmit_bytes_total counter
fortiwlc_transmit_bytes_total{ap_name="w1-tolos.cpe.arnes.si",campus="volantis",interface="eth0",wlc="wlc.ansoext.arnes.si"} 0.0
fortiwlc_transmit_bytes_total{ap_name="w1-volantis.cpe.arnes.si",campus="volantis",interface="eth0",wlc="wlc.ansoext.arnes.si"} 0.0
# HELP fortiwlc_receive_packets_total Wired metrics
# TYPE fortiwlc_receive_packets_total counter
fortiwlc_receive_packets_total{ap_name="w1-tolos.cpe.arnes.si",campus="volantis",interface="eth0",wlc="wlc.ansoext.arnes.si"} 0.0
fortiwlc_receive_packets_total{ap_name="w1-volantis.cpe.arnes.si",campus="volantis",interface="eth0",wlc="wlc.ansoext.arnes.si"} 0.0
# HELP fortiwlc_transmit_packets_total Wired metrics
# TYPE fortiwlc_transmit_packets_total counter
fortiwlc_transmit_packets_total{ap_name="w1-tolos.cpe.arnes.si",campus="volantis",interface="eth0",wlc="wlc.ansoext.arnes.si"} 0.0
fortiwlc_transmit_packets_total{ap_name="w1-volantis.cpe.arnes.si",campus="volantis",interface="eth0",wlc="wlc.ansoext.arnes.si"} 0.0
# HELP fortiwlc_receive_errs_total Wired metrics
# TYPE fortiwlc_receive_errs_total counter
fortiwlc_receive_errs_total{ap_name="w1-tolos.cpe.arnes.si",campus="volantis",interface="eth0",wlc="wlc.ansoext.arnes.si"} 0.0
fortiwlc_receive_errs_total{ap_name="w1-volantis.cpe.arnes.si",campus="volantis",interface="eth0",wlc="wlc.ansoext.arnes.si"} 0.0
# HELP fortiwlc_transmit_errs_total Wired metrics
# TYPE fortiwlc_transmit_errs_total counter
fortiwlc_transmit_errs_total{ap_name="w1-tolos.cpe.arnes.si",campus="volantis",interface="eth0",wlc="wlc.ansoext.arnes.si"} 0.0
fortiwlc_transmit_errs_total{ap_name="w1-volantis.cpe.arnes.si",campus="volantis",interface="eth0",wlc="wlc.ansoext.arnes.si"} 0.0
# HELP fortiwlc_receive_drop_total Wired metrics
# TYPE fortiwlc_receive_drop_total counter
fortiwlc_receive_drop_total{ap_name="w1-tolos.cpe.arnes.si",campus="volantis",interface="eth0",wlc="wlc.ansoext.arnes.si"} 0.0
fortiwlc_receive_drop_total{ap_name="w1-volantis.cpe.arnes.si",campus="volantis",interface="eth0",wlc="wlc.ansoext.arnes.si"} 0.0
# HELP fortiwlc_transmit_drop_total Wired metrics
# TYPE fortiwlc_transmit_drop_total counter
fortiwlc_transmit_drop_total{ap_name="w1-tolos.cpe.arnes.si",campus="volantis",interface="eth0",wlc="wlc.ansoext.arnes.si"} 0.0
fortiwlc_transmit_drop_total{ap_name="w1-volantis.cpe.arnes.si",campus="volantis",interface="eth0",wlc="wlc.ansoext.arnes.si"} 0.0
# HELP fortiwlc_transmit_colls_total Wired metrics
# TYPE fortiwlc_transmit_colls_total counter
fortiwlc_transmit_colls_total{ap_name="w1-tolos.cpe.arnes.si",campus="volantis",interface="eth0",wlc="wlc.ansoext.arnes.si"} 0.0
fortiwlc_transmit_colls_total{ap_name="w1-volantis.cpe.arnes.si",campus="volantis",interface="eth0",wlc="wlc.ansoext.arnes.si"} 0.0
```

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
poetry run python fortiwlc_exporter/exporter.py
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
