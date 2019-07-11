import logging
from collections import defaultdict

from prometheus_client.core import GaugeMetricFamily, InfoMetricFamily

from fortiwlc_exporter import settings
from fortiwlc_exporter.exceptions import ExporterConfigError
from fortiwlc_exporter.fortiwlc import FortiWLC
from fortiwlc_exporter.parsers import parse_ap_data, parse_wifi_name
from fortiwlc_exporter.utils import timeit


class FortiwlcCollector:
    def __init__(self, hosts):
        self.wlcs = self.init_wlcs(hosts)
        self.init_data()

    def init_data(self):
        self.ap_info = {}
        self.clients = defaultdict(int)
        self.radio_types = set(
            ['802.11ac', '802.11g', '802.11n', '802.11n-5G', 'unknown']
        )
        self.wifi_info = {}

    def init_wlcs(self, names):
        """ Initializes FortiWLC instances """
        wlcs = []
        for name in names:
            if settings.WLC_API_KEY:
                wlcs.append(FortiWLC(name=name, api_key=settings.WLC_API_KEY))
            elif settings.WLC_USERNAME:
                wlcs.append(
                    FortiWLC(
                        name=name,
                        username=settings.WLC_USERNAME,
                        password=settings.WLC_PASSWORD,
                    )
                )
            else:
                raise ExporterConfigError(
                    'Missing WLC_USERNAME and WLC_PASSWORD or WLC_API_KEY in configuration'
                )
        return wlcs

    def init_metrics(self):
        self.fortiwlc_clients = GaugeMetricFamily(
            'fortiwlc_clients',
            'Number of clients connected to a specific combination of access '
            'point, radio and wifi network in a campus.',
            labels=['ap_name', 'radio_type', 'wifi_network', 'campus'],
        )
        self.fortiwlc_ap_info = InfoMetricFamily(
            'fortiwlc_ap',
            'Access point information',
            labels=[
                'wlc',
                'ap_name',
                'ap_status',
                'ap_state',
                'os_version',
                'profile',
                'model',
                'campus',
            ],
        )
        self.fortiwlc_wifi_info = InfoMetricFamily(
            'fortiwlc_wifi',
            'Wireless network (SSID) information',
            labels=['wifi_network', 'ssid'],
        )
        self.fortiwlc_up = GaugeMetricFamily(
            'fortiwlc_up',
            'Was the last scrape of data from FortiNET WLC instance successful.',
            labels=['wlc'],
        )

    def describe(self):
        self.init_metrics()
        yield self.fortiwlc_clients
        yield self.fortiwlc_ap_info
        yield self.fortiwlc_wifi_info
        yield self.fortiwlc_up

    @timeit
    def collect(self):
        self.init_metrics()

        try:
            self.poll_wlcs()
            self.parse_metrics()
        except Exception as e:
            if settings.DEBUG:
                raise
            logging.error('Error polling or parsing metrics', exc_info=e)
            self.fortiwlc_up.add_metric([], 0)
        else:
            for wlc in self.wlcs:
                self.fortiwlc_up.add_metric([wlc.name], int(wlc.last_pool_ok))

        try:
            for key, count in self.clients.items():
                ap_info = self.ap_info[key[0]]
                if len(ap_info) > 7:
                    campus = ap_info[7]
                    self.fortiwlc_clients.add_metric(key + (campus,), count)
                else:
                    self.fortiwlc_clients.add_metric(key, count)

            for _, labels in self.ap_info.items():
                self.fortiwlc_ap_info.add_metric(labels, {})

            for _, labels in self.wifi_info.items():
                self.fortiwlc_wifi_info.add_metric(labels, {})
        except Exception as e:
            if settings.DEBUG:
                raise
            logging.error('Error returning metrics', exc_info=e)
            self.fortiwlc_up.add_metric([], 0)

        yield self.fortiwlc_clients
        yield self.fortiwlc_ap_info
        yield self.fortiwlc_wifi_info
        yield self.fortiwlc_up

    @timeit
    def poll_wlcs(self):
        """ Polls all data from all WLCs APIs """
        for wlc in self.wlcs:
            wlc.poll()

    @timeit
    def parse_metrics(self):
        """ Parses collected WLC data """
        self.init_data()
        self.parse_by_ssid()
        self.parse_by_ap()

    def parse_by_ap(self):
        """ Generates labels for each AP/radio/SSID combo """
        for wlc in self.wlcs:
            for ap_data in wlc.managed_ap:
                ap = parse_ap_data(ap_data, wlc.name)
                self.ap_info[ap[1]] = ap

                wifi_networks = self.get_wifi_networks(ap_data, wlc)
                for wifi_network in wifi_networks:
                    self.wifi_info[wifi_network[0]] = wifi_network
                    for radio_type in self.radio_types:
                        self.clients[
                            (ap_data['name'], radio_type, wifi_network[0])
                        ] += 0

    def parse_by_ssid(self):
        """ Counts clients on each AP/radio type/SSID combo """
        for wlc in self.wlcs:
            for client in wlc.clients:
                # sometimes we see malformed data
                try:
                    key = (client['wtp_name'], client['radio_type'], client['vap_name'])
                except KeyError:
                    logging.error('KeyError for client entry: {}'.format(client))
                    continue
                self.clients[key] += 1
                self.radio_types.add(client['radio_type'])
                self.wifi_info[client['vap_name']] = (
                    client['vap_name'],
                    client['ssid'],
                )

    def get_wifi_networks(self, ap, wlc):
        wifi_networks = []
        for radio_data in ap['radio']:
            for ssid_key in radio_data.get('ssid', {}).keys():
                try:
                    group = next(filter(lambda g: g['name'] == ssid_key, wlc.vap_group))
                except StopIteration:
                    wifi_networks.append(parse_wifi_name(ssid_key))
                else:
                    for vap_data in group['vaps']:
                        wifi_networks.append(parse_wifi_name(vap_data['name']))
        return wifi_networks
