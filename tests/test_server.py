import json
import unittest
import responses
import requests

from exporter import start_server


class TestServer(unittest.TestCase):
    def setUp(self):
        self.port = 23344
        self.config = {'port': self.port, 'wlcs': [{'name': 'wlc.ansoext.arnes.si', 'api_key': 'r8g1y84z1q73x96s91gQq0pfGNd4x7'}]}

    @responses.activate
    def test_output(self):
        """ Test if exporter http server returns expected data """
        responses.add(
            responses.GET,
            'https://wlc.ansoext.arnes.si/api/v2/monitor/wifi/managed_ap/select/?vdom=root&access_token=r8g1y84z1q73x96s91gQq0pfGNd4x7',
            json=json.load(open('./tests/data/wlc.ansoext.arnes.si-managed_ap-200.json')),
            status=200
        )
        responses.add(
            responses.GET,
            'https://wlc.ansoext.arnes.si/api/v2/cmdb/wireless-controller/vap-group/?vdom=root&access_token=r8g1y84z1q73x96s91gQq0pfGNd4x7',
            json=json.load(open('./tests/data/wlc.ansoext.arnes.si-vap_group-200.json')),
            status=200
        )
        responses.add(
            responses.GET,
            'https://wlc.ansoext.arnes.si/api/v2/monitor/wifi/client/select/?vdom=root&access_token=r8g1y84z1q73x96s91gQq0pfGNd4x7',
            json=json.load(open('./tests/data/wlc.ansoext.arnes.si-client-1-200.json')),
            status=200
        )
        responses.add_passthru('http://localhost:{}'.format(self.port))
        expected_lines = open('./tests/data/wlc.ansoext.arnes.si-managed_ap-200.result').read().splitlines()

        start_server(self.config)
        self.assertEqual(len(responses.calls), 3)
        r = requests.get('http://localhost:{}'.format(self.port))
        r.raise_for_status()
        self.assertEqual(len(responses.calls), 6)
        resp_lines = [l for l in r.text.split('\n') if 'fortiwlc' in l]
        print(resp_lines)
        self.assertEqual(resp_lines, expected_lines)
