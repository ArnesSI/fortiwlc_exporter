#!/usr/bin/env python

import argparse
import time
from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY

from fortiwlc_exporter import __version__
from fortiwlc_exporter.collector import FortiwlcCollector
from fortiwlc_exporter.config import get_config


def start_server(config):
    REGISTRY.register(FortiwlcCollector(config))
    start_http_server(config['port'])


def main():
    parser = argparse.ArgumentParser(
        prog='fortiwlc_exporter', description='FortiOS WLC Prometheus Collector'
    )
    parser.add_argument(
        '-c',
        dest='config_file',
        help='Configuration file',
        default='fortiwlc_exporter.ini',
        type=argparse.FileType('r'),
    )
    parser.add_argument('--debug', action='store_true')
    parser.add_argument(
        '--version', action='version', version='%(prog)s {}'.format(__version__)
    )
    args = parser.parse_args()
    config = get_config(args.config_file, extra=args)
    start_server(config)
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
