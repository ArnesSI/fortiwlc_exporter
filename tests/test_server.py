import json
import unittest
import responses
import requests
from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY

from fortiwlc_exporter import FortiwlcCollector


class TestServer(unittest.TestCase):
    """ Test if exporter http server returns expected data """
    
    @responses.activate
    def setUp(self):
        self.port = 23344
        responses.add(
            responses.GET,
            'https://wlc.ansoext.arnes.si/api/v2/monitor/wifi/managed_ap/select/?vdom=root&access_token=r8g1y84z1q73x96s91gQq0pfGNd4x7',
            json=json.load(open('./tests/data/wlc.ansoext.arnes.si-managed_ap-200.json')),
            status=200
        )
        REGISTRY.register(FortiwlcCollector())
        start_http_server(self.port)

    @responses.activate
    def test_output(self):
        responses.add(
            responses.GET,
            'https://wlc.ansoext.arnes.si/api/v2/monitor/wifi/managed_ap/select/?vdom=root&access_token=r8g1y84z1q73x96s91gQq0pfGNd4x7',
            json=json.load(open('./tests/data/wlc.ansoext.arnes.si-managed_ap-200.json')),
            status=200
        )
        responses.add_passthru('http://localhost:{}'.format(self.port))
        r = requests.get('http://localhost:{}'.format(self.port))
        r.raise_for_status()
        self.assertEqual(len(responses.calls), 1)
        resp_lines = r.text.split('\n')
        for expected_line in open('./tests/data/wlc.ansoext.arnes.si-managed_ap-200.result'):
            self.assertIn(expected_line.rstrip('\n'), resp_lines)
