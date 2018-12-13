import json
import unittest

from fortiwlc_exporter.parsers import parse_ap_data, parse_wifi_name


class TestApParser(unittest.TestCase):
    def test_parse_ap_data(self):
        ap_data = json.load(open('./tests/data/wlc.ansoext.arnes.si-managed_ap-200.json'))['results'][0]
        expected_data = {
            "name": "w1-tolos.cpe.arnes.si",
            "campus_name": "tolos",
            "profile_name": "tolos_FAP221E",
            "model": "FAP221E",
            "wlc": "mywlc",
            "status": "connected",
            "state": "authorized",
            "client_count": 6,
            "per_radio": {"1": 4, "2": 2},
            "ssid": {"ssid": "", "campus_id": "", "radious_group": ""}
        }
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
