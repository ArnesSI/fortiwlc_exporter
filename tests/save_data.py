#!/usr/bin/env python

# Script to save API data from WLC. Call as:
# tests/save_data.py hostname username output_dir/

import argparse
import getpass
import json
import os

from fortiwlc_exporter.fortiwlc import FortiWLC

parser = argparse.ArgumentParser(description='Save needed API data from FortiOS WLC')
parser.add_argument('host')
parser.add_argument('username')
parser.add_argument('output_directory')
args = parser.parse_args()

password = getpass.getpass('WLC password: ')

wlc = FortiWLC(args.host, username=args.username, password=password)
path = os.path.join(args.output_directory, args.host + '-{}.json')
try:
    os.mkdir(args.output_directory)
except FileExistsError:
    pass

json.dump(
    wlc.get_managed_ap(), open(path.format('managed_ap'), 'w'), indent=4, sort_keys=True
)
json.dump(
    wlc.get_vap_group(), open(path.format('vap_group'), 'w'), indent=4, sort_keys=True
)
json.dump(
    wlc.get_clients(), open(path.format('clients'), 'w'), indent=4, sort_keys=True
)
