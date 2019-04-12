import argparse
import logging
import signal
import sys
import time

import yaml
from prometheus_client import REGISTRY, CollectorRegistry, start_http_server

from fortiwlc_exporter import __version__, settings
from fortiwlc_exporter.collector import FortiwlcCollector
from fortiwlc_exporter.exceptions import ExporterConfigError


def setup_logging():
    """Setup logging to console"""
    logging.basicConfig(
        level=logging.DEBUG if settings.DEBUG else logging.INFO,
        format='%(levelname)s - %(message)s',
    )
    handler = logging.StreamHandler(sys.stderr)
    logging.getLogger().addHandler(handler)


def parse_settings(cmd_args):
    """Parse config file and command line arguments"""
    config_parser = argparse.ArgumentParser(
        description='Prometheus exporter for FortiOS WLC', add_help=False
    )
    config_parser.add_argument(
        '-V', '--version', action='version', version='%(prog)s {}'.format(__version__)
    )
    config_parser.add_argument(
        '-c',
        dest='config_file',
        help='Configuration file in YAML format',
        type=argparse.FileType('r'),
    )
    args, remaining_argv = config_parser.parse_known_args(cmd_args)

    parse_config_file(args.config_file)

    parser = argparse.ArgumentParser(parents=[config_parser])
    parser.set_defaults(
        debug=settings.DEBUG,
        no_default_collectors=settings.NO_DEFAULT_COLLECTORS,
        timeout=settings.TIMEOUT,
        exporter_port=settings.EXPORTER_PORT,
    )
    parser.add_argument(
        '-d', '--debug', dest='debug', action='store_true', help='debug mode'
    )
    # parser.add_argument(
    #     '-1',
    #     dest='one_off',
    #     action='store_true',
    #     help='collect and parse metrics once, print them and exit',
    # )
    parser.add_argument(
        '--no-default-collectors',
        dest='no_default_collectors',
        action='store_true',
        help='disable process, gc and other default collectors',
    )
    parser.add_argument(
        '--timeout',
        dest='timeout',
        type=int,
        help='Timeout in seconds to generate a reply (default 60)',
    )
    parser.add_argument(
        '--exporter-port',
        dest='exporter_port',
        type=int,
        help='TCP port exporter should listen on (default 9118)',
    )
    args = parser.parse_args(remaining_argv)

    settings.DEBUG = args.debug
    # settings.ONE_OFF = args.one_off
    settings.NO_DEFAULT_COLLECTORS = args.no_default_collectors
    settings.TIMEOUT = args.timeout
    settings.EXPORTER_PORT = args.exporter_port


def parse_config_file(config_file):
    if not config_file:
        return None
    try:
        config = yaml.safe_load(config_file)
    except yaml.parser.ParserError:
        raise ExporterConfigError('Could not parse configuration file.')
    if not config:
        return None

    settings.DEBUG = config.get('debug', settings.DEBUG)
    settings.NO_DEFAULT_COLLECTORS = config.get(
        'no_default_collectors', settings.NO_DEFAULT_COLLECTORS
    )

    settings.TIMEOUT = config.get('timeout', settings.TIMEOUT)

    settings.EXPORTER_PORT = config.get('exporter_port', settings.EXPORTER_PORT)

    settings.WLC_USERNAME = config.get('wlc_username', settings.WLC_USERNAME)
    settings.WLC_PASSWORD = config.get('wlc_password', settings.WLC_PASSWORD)

    settings.WLC_API_KEY = config.get('wlc_api_key', settings.WLC_API_KEY)

    settings.WLCS = config.get('wlcs', settings.WLCS)
    settings.WORKERS = config.get('workers', settings.WORKERS)


def stop_exporter(signum, frame):
    logging.info('fortiwlc_exporter shutting down')
    sys.exit(0)


def start_exporter():
    """Register the collector and start exporter https server"""
    # handle singals to shutdown gracefully
    signal.signal(signal.SIGINT, stop_exporter)
    signal.signal(signal.SIGTERM, stop_exporter)

    if settings.NO_DEFAULT_COLLECTORS:
        registry = CollectorRegistry()
    else:
        registry = REGISTRY
    registry.register(FortiwlcCollector(hosts=settings.WLCS))
    logging.info('fortiwlc_exporter starting on port {}'.format(settings.EXPORTER_PORT))
    start_http_server(settings.EXPORTER_PORT, registry=registry)
    while True:
        time.sleep(1)


def main():
    parse_settings(sys.argv[1:])
    setup_logging()
    if settings.ONE_OFF:
        import json

        a = FortiwlcCollector(hosts=settings.WLCS).get_metrics()
        print(json.dumps(a, indent=4))
        sys.exit(0)
    else:
        start_exporter()


if __name__ == "__main__":
    main()
