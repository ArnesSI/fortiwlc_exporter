import json
import unittest

from fortiwlc_exporter.parsers import get_ap_os_version, parse_ap_data, parse_wifi_name


class TestApParser(unittest.TestCase):
    def test_parse_ap_data(self):
        ap_data = json.load(
            open('./tests/data/one_client/wlc.ansoext.arnes.si-managed_ap.json')
        )['results'][0]
        expected_data = [
            "mywlc",
            "w1-tolos.cpe.arnes.si",
            "connected",
            "authorized",
            'v5.6-build6508',
            "tolos_FAP221E",
            "FAP221E",
            "tolos",
        ]
        parsed = parse_ap_data(ap_data, 'mywlc')
        self.assertEqual(parsed, expected_data)

    def test_parse_wifi_name(self):
        self.assertEqual(parse_wifi_name('1_wifi'), ('1_wifi', 'wifi'))
        self.assertEqual(parse_wifi_name('1_wifi_new'), ('1_wifi_new', 'wifi_new'))
        self.assertEqual(parse_wifi_name('wifi'), ('wifi', 'wifi'))


class TestApOsVersion(unittest.TestCase):
    def test_has_version_unparsable(self):
        self.assertEqual(get_ap_os_version({'os_version': 'abc'}), 'abc')

    def test_has_version_parsable(self):
        self.assertEqual(
            get_ap_os_version({'os_version': 'FP221E-v6.0-build0033'}), 'v6.0-build0033'
        )

    def test_no_version(self):
        self.assertEqual(get_ap_os_version({}), 'unknown')
