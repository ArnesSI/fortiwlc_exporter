import json
import unittest
import responses
from unittest.mock import MagicMock

from fortiwlc_exporter.collector import FortiwlcCollector
from fortiwlc_exporter.fortiwlc import FortiWLC


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


class TestCollectorInit(unittest.TestCase):
    ''' Testing collector initialization '''

    def test_init(self):
        ''' Test initialization of collector '''
        config = {'workers': 1, 'wlcs': [{'name': 'mywlc', 'api_key': '123'}]}
        c = FortiwlcCollector(config)
        self.assertEqual(len(c.wlcs), 1)
        self.assertIsInstance(c.wlcs[0], FortiWLC)
        self.assertEqual(c.wlcs[0].name, 'mywlc')
        self.assertEqual(c.ap_info, {})
        self.assertEqual(c.clients, {})
        self.assertEqual(
            c.radio_types,
            set(['802.11ac', '802.11g', '802.11n', '802.11n-5G', 'unknown']),
        )
        self.assertEqual(c.wifi_info, {})


class TestCollectorPoll(unittest.TestCase):
    ''' Testing polling methods '''

    @responses.activate
    def test_poll(self):
        ''' Test polling function '''
        test_case = 'no_clients'
        host = 'wlc.ansoext.arnes.si'
        config = {'workers': 1, 'wlcs': [{'name': host, 'api_key': '123'}]}
        responses_add(test_case, host, 'clients')
        responses_add(test_case, host, 'vap_group')
        responses_add(test_case, host, 'managed_ap')
        col = FortiwlcCollector(config)
        self.assertEqual(len(col.wlcs), 1)
        col.poll_wlcs()
        self.assertEqual(len(responses.calls), 3)


class TestCollectorParse(unittest.TestCase):
    ''' Testing parsing methods '''

    @responses.activate
    def test_parse_no_clients(self):
        ''' Test parsing wlc with no clients '''
        test_case = 'no_clients'
        host = 'wlc.ansoext.arnes.si'
        config = {'workers': 1, 'wlcs': [{'name': host, 'api_key': '123'}]}
        responses_add(test_case, host, 'clients')
        responses_add(test_case, host, 'vap_group')
        responses_add(test_case, host, 'managed_ap')
        col = FortiwlcCollector(config)
        self.assertEqual(len(col.wlcs), 1)
        col.poll_wlcs()
        self.assertEqual(len(responses.calls), 3)
        col.parse_metrics()
        print(col.clients)
        self.assertEqual(
            col.clients,
            {
                ('w1-tolos.cpe.arnes.si', '802.11g', '1_eduroam'): 0,
                ('w1-tolos.cpe.arnes.si', '802.11ac', '1_eduroam'): 0,
                ('w1-tolos.cpe.arnes.si', '802.11n', '1_eduroam'): 0,
                ('w1-tolos.cpe.arnes.si', '802.11n-5G', '1_eduroam'): 0,
                ('w1-tolos.cpe.arnes.si', 'unknown', '1_eduroam'): 0,
                ('w1-tolos.cpe.arnes.si', '802.11g', '1_tolos_psk'): 0,
                ('w1-tolos.cpe.arnes.si', '802.11ac', '1_tolos_psk'): 0,
                ('w1-tolos.cpe.arnes.si', '802.11n', '1_tolos_psk'): 0,
                ('w1-tolos.cpe.arnes.si', '802.11n-5G', '1_tolos_psk'): 0,
                ('w1-tolos.cpe.arnes.si', 'unknown', '1_tolos_psk'): 0,
                ('w1-volantis.cpe.arnes.si', '802.11g', '2_eduroam'): 0,
                ('w1-volantis.cpe.arnes.si', '802.11ac', '2_eduroam'): 0,
                ('w1-volantis.cpe.arnes.si', '802.11n', '2_eduroam'): 0,
                ('w1-volantis.cpe.arnes.si', '802.11n-5G', '2_eduroam'): 0,
                ('w1-volantis.cpe.arnes.si', 'unknown', '2_eduroam'): 0,
            },
        )
        self.assertEqual(
            col.ap_info,
            {
                'w1-tolos.cpe.arnes.si': [
                    'wlc.ansoext.arnes.si',
                    'w1-tolos.cpe.arnes.si',
                    'connected',
                    'authorized',
                    'tolos_FAP221E',
                    'FAP221E',
                    'tolos',
                ],
                'w1-volantis.cpe.arnes.si': [
                    'wlc.ansoext.arnes.si',
                    'w1-volantis.cpe.arnes.si',
                    'connected',
                    'authorized',
                    'volantis_FAP221E',
                    'FAP221E',
                    'volantis',
                ],
            },
        )
        self.assertEqual(
            col.wifi_info,
            {
                '1_eduroam': ('1_eduroam', 'eduroam'),
                '1_tolos_psk': ('1_tolos_psk', 'tolos_psk'),
                '2_eduroam': ('2_eduroam', 'eduroam'),
            },
        )
        self.assertEqual(
            col.radio_types,
            set(['802.11ac', '802.11g', '802.11n', '802.11n-5G', 'unknown']),
        )

    @responses.activate
    def test_parse_one_client(self):
        ''' Test parsing wlc with no clients '''
        test_case = 'one_client'
        host = 'wlc.ansoext.arnes.si'
        config = {'workers': 1, 'wlcs': [{'name': host, 'api_key': '123'}]}
        responses_add(test_case, host, 'clients')
        responses_add(test_case, host, 'vap_group')
        responses_add(test_case, host, 'managed_ap')
        col = FortiwlcCollector(config)
        self.assertEqual(len(col.wlcs), 1)
        col.poll_wlcs()
        self.assertEqual(len(responses.calls), 3)
        col.parse_metrics()
        self.assertEqual(
            col.clients,
            {
                ('w1-tolos.cpe.arnes.si', '802.11g', '1_eduroam'): 0,
                ('w1-tolos.cpe.arnes.si', '802.11ac', '1_eduroam'): 0,
                ('w1-tolos.cpe.arnes.si', '802.11n', '1_eduroam'): 0,
                ('w1-tolos.cpe.arnes.si', '802.11n-5G', '1_eduroam'): 0,
                ('w1-tolos.cpe.arnes.si', 'unknown', '1_eduroam'): 0,
                ('w1-tolos.cpe.arnes.si', '802.11g', '1_tolos_psk'): 0,
                ('w1-tolos.cpe.arnes.si', '802.11ac', '1_tolos_psk'): 1,
                ('w1-tolos.cpe.arnes.si', '802.11n', '1_tolos_psk'): 0,
                ('w1-tolos.cpe.arnes.si', '802.11n-5G', '1_tolos_psk'): 0,
                ('w1-tolos.cpe.arnes.si', 'unknown', '1_tolos_psk'): 0,
                ('w1-volantis.cpe.arnes.si', '802.11g', '2_eduroam'): 0,
                ('w1-volantis.cpe.arnes.si', '802.11ac', '2_eduroam'): 0,
                ('w1-volantis.cpe.arnes.si', '802.11n', '2_eduroam'): 0,
                ('w1-volantis.cpe.arnes.si', '802.11n-5G', '2_eduroam'): 0,
                ('w1-volantis.cpe.arnes.si', 'unknown', '2_eduroam'): 0,
            },
        )
        self.assertEqual(
            col.ap_info,
            {
                'w1-tolos.cpe.arnes.si': [
                    'wlc.ansoext.arnes.si',
                    'w1-tolos.cpe.arnes.si',
                    'connected',
                    'authorized',
                    'tolos_FAP221E',
                    'FAP221E',
                    'tolos',
                ],
                'w1-volantis.cpe.arnes.si': [
                    'wlc.ansoext.arnes.si',
                    'w1-volantis.cpe.arnes.si',
                    'connected',
                    'authorized',
                    'volantis_FAP221E',
                    'FAP221E',
                    'volantis',
                ],
            },
        )
        self.assertEqual(
            col.wifi_info,
            {
                '1_eduroam': ('1_eduroam', 'eduroam'),
                '1_tolos_psk': ('1_tolos_psk', 'tolos_psk'),
                '2_eduroam': ('2_eduroam', 'eduroam'),
            },
        )
        self.assertEqual(
            col.radio_types,
            set(['802.11ac', '802.11g', '802.11n', '802.11n-5G', 'unknown']),
        )

    @responses.activate
    def test_parse_many_clients(self):
        ''' Test parsing wlc with no clients '''
        test_case = 'many_clients'
        host1 = 'wlc1.anso.arnes.si'
        host2 = 'wlc2.anso.arnes.si'
        config = {
            'workers': 1,
            'wlcs': [
                {'name': host1, 'api_key': '123'},
                {'name': host2, 'api_key': '123'},
            ],
        }
        responses_add(test_case, host1, 'clients')
        responses_add(test_case, host1, 'vap_group')
        responses_add(test_case, host1, 'managed_ap')
        responses_add(test_case, host2, 'clients')
        responses_add(test_case, host2, 'vap_group')
        responses_add(test_case, host2, 'managed_ap')
        col = FortiwlcCollector(config)
        self.assertEqual(len(col.wlcs), 2)
        col.poll_wlcs()
        self.assertEqual(len(responses.calls), 6)
        col.parse_metrics()
        self.assertEqual(len(col.clients), 8910)
        self.assertEqual(len(col.ap_info), 1640)
        self.assertEqual(len(col.wifi_info), 90)
        self.assertEqual(len(col.radio_types), 5)

    @responses.activate
    def test_parse_extra_radio(self):
        ''' Test if a new radio type appears in clients endpoint '''
        test_case = 'extra_radio'
        host = 'wlc.ansoext.arnes.si'
        config = {'workers': 1, 'wlcs': [{'name': host, 'api_key': '123'}]}
        responses_add(test_case, host, 'clients')
        responses_add(test_case, host, 'vap_group')
        responses_add(test_case, host, 'managed_ap')
        col = FortiwlcCollector(config)
        self.assertEqual(len(col.wlcs), 1)
        col.poll_wlcs()
        self.assertEqual(len(responses.calls), 3)
        col.parse_metrics()
        self.assertIn('extra.radio', col.radio_types)
        self.assertEqual(
            col.clients,
            {
                ('w1-tolos.cpe.arnes.si', '802.11g', '1_eduroam'): 0,
                ('w1-tolos.cpe.arnes.si', '802.11ac', '1_eduroam'): 0,
                ('w1-tolos.cpe.arnes.si', '802.11n', '1_eduroam'): 0,
                ('w1-tolos.cpe.arnes.si', '802.11n-5G', '1_eduroam'): 0,
                ('w1-tolos.cpe.arnes.si', 'unknown', '1_eduroam'): 0,
                ('w1-tolos.cpe.arnes.si', 'extra.radio', '1_eduroam'): 0,
                ('w1-tolos.cpe.arnes.si', '802.11g', '1_tolos_psk'): 0,
                ('w1-tolos.cpe.arnes.si', '802.11ac', '1_tolos_psk'): 0,
                ('w1-tolos.cpe.arnes.si', '802.11n', '1_tolos_psk'): 0,
                ('w1-tolos.cpe.arnes.si', '802.11n-5G', '1_tolos_psk'): 0,
                ('w1-tolos.cpe.arnes.si', 'unknown', '1_tolos_psk'): 0,
                ('w1-tolos.cpe.arnes.si', 'extra.radio', '1_tolos_psk'): 1,
                ('w1-volantis.cpe.arnes.si', '802.11g', '2_eduroam'): 0,
                ('w1-volantis.cpe.arnes.si', '802.11ac', '2_eduroam'): 0,
                ('w1-volantis.cpe.arnes.si', '802.11n', '2_eduroam'): 0,
                ('w1-volantis.cpe.arnes.si', '802.11n-5G', '2_eduroam'): 0,
                ('w1-volantis.cpe.arnes.si', 'unknown', '2_eduroam'): 0,
                ('w1-volantis.cpe.arnes.si', 'extra.radio', '2_eduroam'): 0,
            },
        )


class TestCollectorCollect(unittest.TestCase):
    ''' Testing collect method '''

    @responses.activate
    def test_collect_no_clients(self):
        host = 'wlc.ansoext.arnes.si'
        config = {'workers': 1, 'wlcs': [{'name': host, 'api_key': '123'}]}

        col = FortiwlcCollector(config)
        col.poll_wlcs = MagicMock()
        col.parse_metrics = MagicMock()
        col.wlcs[0].last_pool_ok = True

        for metric in col.collect():
            if metric.name == 'fortiwlc_up':
                self.assertEqual(len(metric.samples), 1)
                self.assertEqual(metric.samples[0].value, 1)
                self.assertEqual(
                    metric.samples[0].labels, {'wlc': 'wlc.ansoext.arnes.si'}
                )
            elif metric.name == 'fortiwlc_clients':
                self.assertEqual(len(metric.samples), 0)
            elif metric.name == 'fortiwlc_ap':
                self.assertEqual(len(metric.samples), 0)
            elif metric.name == 'fortiwlc_wifi':
                self.assertEqual(len(metric.samples), 0)
            else:
                raise Exception('Unknown metric {}'.format(metric))
        col.poll_wlcs.assert_called_once()
        col.parse_metrics.assert_called_once()
