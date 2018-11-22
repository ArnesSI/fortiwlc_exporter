import json
import unittest
import responses
import requests
from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY

from exporter import start_server


class TestServer(unittest.TestCase):

    @responses.activate
    def test_output(self):
        """ Test if exporter http server returns expected data """
        port = 23344
        responses.add(
            responses.GET,
            'https://wlc.ansoext.arnes.si/api/v2/monitor/wifi/managed_ap/select/?vdom=root&access_token=r8g1y84z1q73x96s91gQq0pfGNd4x7',
            json=json.load(open('./tests/data/wlc.ansoext.arnes.si-managed_ap-200.json')),
            status=200
        )
        responses.add_passthru('http://localhost:{}'.format(port))
        start_server('testing', port)
        self.assertEqual(len(responses.calls), 1)
        r = requests.get('http://localhost:{}'.format(port))
        r.raise_for_status()
        self.assertEqual(len(responses.calls), 2)
        resp_lines = r.text.split('\n')
        for expected_line in open('./tests/data/wlc.ansoext.arnes.si-managed_ap-200.result'):
            self.assertIn(expected_line.rstrip('\n'), resp_lines)
