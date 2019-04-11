#!/usr/bin/env python

# Script to save API data from WLC. Call as:
# tests/save_data.py hostname api_key output_dir/

import argparse
import json
import os

from fortiwlc_exporter.fortiwlc import FortiWLC

parser = argparse.ArgumentParser(description='Save needed API data from FortiOS WLC')
parser.add_argument('host')
parser.add_argument('api_key')
parser.add_argument('output_directory')
args = parser.parse_args()

wlc = FortiWLC(args.host, args.api_key)
wlc.poll()
path = os.path.join(args.output_directory, args.host + '-{}.json')

json.dump(
    wlc.managed_ap, open(path.format('managed_ap'), 'w'), indent=4, sort_keys=True
)
json.dump(wlc.vap_group, open(path.format('vap_group'), 'w'), indent=4, sort_keys=True)
json.dump(wlc.clients, open(path.format('clients'), 'w'), indent=4, sort_keys=True)
