import json
import responses
import unittest

from fortiwlc_exporter.fortiwlc import FortiWLC


class TestFortiWLC(unittest.TestCase):
    @responses.activate
    def test_managed_ap_ok(self):
        """ Test successfull API call for managed APs """
        url = 'https://wlc.ansoext.arnes.si/api/v2/monitor/wifi/managed_ap/select/?vdom=root&access_token=123'
        response_data = json.load(open('./tests/data/wlc.ansoext.arnes.si-managed_ap-200.json'))
        responses.add(
            responses.GET,
            url,
            json=response_data,
            status=200
        )
        wlc = FortiWLC('wlc.ansoext.arnes.si', '123')
        wlc_data = wlc.get_managed_ap()
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(wlc.name, 'wlc.ansoext.arnes.si')
        self.assertEqual(wlc.api_key, '123')
        self.assertEqual(wlc_data, response_data['results'])

    @responses.activate
    def test_vap_group_ok(self):
        """ Test successfull API call for managed APs """
        url = 'https://wlc.ansoext.arnes.si/api/v2/cmdb/wireless-controller/vap-group/?vdom=root&access_token=123'
        response_data = json.load(open('./tests/data/wlc.ansoext.arnes.si-vap_group-200.json'))
        responses.add(
            responses.GET,
            url,
            json=response_data,
            status=200
        )
        wlc = FortiWLC('wlc.ansoext.arnes.si', '123')
        wlc_data = wlc.get_vap_group()
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(wlc.name, 'wlc.ansoext.arnes.si')
        self.assertEqual(wlc.api_key, '123')
        self.assertEqual(wlc_data, response_data['results'])

    @responses.activate
    def test_clients_none_ok(self):
        """ Test successfull API call for clients """
        url = 'https://wlc.ansoext.arnes.si/api/v2/monitor/wifi/client/select/?vdom=root&access_token=123'
        response_data = json.load(open('./tests/data/wlc.ansoext.arnes.si-client-none-200.json'))
        responses.add(
            responses.GET,
            url,
            json=response_data,
            status=200
        )
        wlc = FortiWLC('wlc.ansoext.arnes.si', '123')
        wlc_data = wlc.get_clients()
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(wlc.name, 'wlc.ansoext.arnes.si')
        self.assertEqual(wlc.api_key, '123')
        self.assertEqual(wlc_data, response_data['results'])

    @responses.activate
    def test_clients_1_ok(self):
        """ Test successfull API call for clients """
        url = 'https://wlc.ansoext.arnes.si/api/v2/monitor/wifi/client/select/?vdom=root&access_token=123'
        response_data = json.load(open('./tests/data/wlc.ansoext.arnes.si-client-1-200.json'))
        responses.add(
            responses.GET,
            url,
            json=response_data,
            status=200
        )
        wlc = FortiWLC('wlc.ansoext.arnes.si', '123')
        wlc_data = wlc.get_clients()
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(wlc.name, 'wlc.ansoext.arnes.si')
        self.assertEqual(wlc.api_key, '123')
        self.assertEqual(wlc_data, response_data['results'])
