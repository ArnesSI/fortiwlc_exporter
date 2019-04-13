import json
import unittest

import requests
import responses
from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY

from fortiwlc_exporter import settings
from fortiwlc_exporter.collector import FortiwlcCollector


def responses_add(test_case, host, resource, method=responses.GET):
    if resource == 'vap_group':
        url = 'https://{}/api/v2/cmdb/wireless-controller/vap-group/?vdom=root'.format(
            host
        )
    elif resource == 'clients':
        url = 'https://{}/api/v2/monitor/wifi/client/select/?vdom=root'.format(host)
    elif resource == 'managed_ap':
        url = 'https://{}/api/v2/monitor/wifi/managed_ap/select/?vdom=root'.format(host)
    response_data = json.load(
        open('./tests/data/{}/{}-{}.json'.format(test_case, host, resource))
    )
    responses.add(method, url, json=response_data, status=200)


class BaseServerRunner(unittest.TestCase):
    def setUp(self):
        self._responses_calls = 0

    def _run_test_case(self):
        for host in self.hosts:
            responses_add(self.test_case, host, 'clients')
            responses_add(self.test_case, host, 'vap_group')
            responses_add(self.test_case, host, 'managed_ap')
        responses.add_passthru('http://localhost:{}'.format(self.port))
        expected_lines = (
            open('./tests/data/{}/result.txt'.format(self.test_case))
            .read()
            .splitlines()
        )

        self.assertEqual(len(responses.calls), 0 + self._responses_calls)
        r = requests.get('http://localhost:{}'.format(self.port))
        r.raise_for_status()
        self.assertEqual(
            len(responses.calls), 3 * len(self.hosts) + self._responses_calls
        )
        resp_lines = [l for l in r.text.split('\n') if 'fortiwlc' in l]

        print('\n'.join(resp_lines))
        print('--- ^ resp ^ --- v expected v ---')
        print('\n'.join(expected_lines))

        expected_lines.sort()
        resp_lines.sort()

        self.assertEqual(resp_lines, expected_lines)
        self._responses_calls = len(responses.calls)


class TestServerOneWLC(BaseServerRunner):
    ''' Test full code stack: starts server and grabs response '''

    @classmethod
    def setUpClass(cls):
        cls.port = 23344
        cls.hosts = ['wlc.ansoext.arnes.si']
        settings.EXPORTER_PORT = cls.port
        settings.WLC_API_KEY = '123'
        cls.collector = FortiwlcCollector(cls.hosts)
        REGISTRY.register(cls.collector)
        start_http_server(cls.port)

    @classmethod
    def tearDownClass(cls):
        REGISTRY.unregister(cls.collector)
        settings.EXPORTER_PORT = 9118
        settings.WLC_API_KEY = None

    @responses.activate
    def test_output_no_clients(self):
        """ Test if exporter http server returns expected data """
        self.test_case = 'no_clients'
        self._run_test_case()

    @responses.activate
    def test_output_one_client(self):
        """ Test if exporter http server returns expected data """
        self.test_case = 'one_client'
        self._run_test_case()


class TestServerTwoWLC(BaseServerRunner):
    ''' Test full code stack: starts server and grabs response '''

    @classmethod
    def setUpClass(cls):
        # can't kill server from above test class. Just start new one on new port
        cls.port = 23345
        cls.hosts = ['wlc1.anso.arnes.si', 'wlc2.anso.arnes.si']
        settings.EXPORTER_PORT = cls.port
        settings.WLC_API_KEY = '123'
        cls.collector = FortiwlcCollector(cls.hosts)
        REGISTRY.register(cls.collector)
        start_http_server(cls.port)

    @classmethod
    def tearDownClass(cls):
        REGISTRY.unregister(cls.collector)
        settings.EXPORTER_PORT = 9118
        settings.WLC_API_KEY = None

    @responses.activate
    def test_output_many_clients(self):
        """ Test if exporter http server returns expected data """
        self.test_case = 'many_clients'
        self._run_test_case()


class TestServerRunTwice(BaseServerRunner):
    ''' Test full code stack: starts server and grabs response '''

    @classmethod
    def setUpClass(cls):
        # can't kill server from above test class. Just start new one on new port
        cls.port = 23346
        cls.hosts = ['wlc.ansoext.arnes.si']
        settings.EXPORTER_PORT = cls.port
        settings.WLC_API_KEY = '123'
        cls.collector = FortiwlcCollector(cls.hosts)
        REGISTRY.register(cls.collector)
        start_http_server(cls.port)

    @classmethod
    def tearDownClass(cls):
        REGISTRY.unregister(cls.collector)
        settings.EXPORTER_PORT = 9118
        settings.WLC_API_KEY = None

    @responses.activate
    def test_output_many_clients(self):
        """ Test if polling twice works ok """
        self.test_case = 'one_client'
        self._run_test_case()
        self._run_test_case()
