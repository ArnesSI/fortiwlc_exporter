import json
import unittest

from fortiwlc_exporter.parsers import parse_ap_data, parse_wifi_name


class TestApParser(unittest.TestCase):
    def test_parse_ap_data(self):
        ap_data = json.load(open('./tests/data/wlc.ansoext.arnes.si-managed_ap-200.json'))['results'][0]
        expected_data = [
            "mywlc",
            "w1-tolos.cpe.arnes.si",
            "connected",
            "authorized",
            "tolos_FAP221E",
            "FAP221E",
            "tolos",
        ]
        parsed = parse_ap_data(ap_data, 'mywlc')
        self.assertEqual(parsed, expected_data)

    def test_parse_wifi_name(self):
        self.assertEqual(
            parse_wifi_name('1_wifi'),
            ('1_wifi', 'wifi')
        )
        self.assertEqual(
            parse_wifi_name('1_wifi_new'),
            ('1_wifi_new', 'wifi_new')
        )
        self.assertEqual(
            parse_wifi_name('wifi'),
            ('wifi', 'wifi')
        )
