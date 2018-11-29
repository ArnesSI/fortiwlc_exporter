from collections import defaultdict, OrderedDict
from prometheus_client.core import GaugeMetricFamily

from .parsers import parse_ap_data, ap_profile_string
from .fortiwlc import FortiWLC


class FortiwlcCollector:
    # order of labels is important if we want to omit some for certain
    # time-series. Those need to be last. Not every ap has wifi networks or
    # a campus, so these are last.
    CLIENTS_LABELS = [
        'wlc',
        'ap_name',
        'ap_status',
        'ap_state',
        'profile',
        'model',
        'radio_id',
        'campus',
        'wifi_network',
        'ssid',
    ]

    def __init__(self, config):
        self.config = config
        self.wlcs = self.init_wlcs()
        self.by_ap = {}
        self.clients = defaultdict(int)

    def init_wlcs(self):
        """ Initializes FortiWLC instances """
        wlcs = []
        for wlc_params in self.config.get('wlcs', []):
            wlcs.append(FortiWLC(**wlc_params))
        return wlcs

    def collect(self):
        fortiwlc_clients = GaugeMetricFamily(
            'fortiwlc_clients',
            'Number of clients connected to a specific combination of access '
            'point, radio and wifi network.',
            labels=self.CLIENTS_LABELS,
        )
        fortiwlc_up = GaugeMetricFamily(
            'fortiwlc_up',
            'Was the last scrape of data from all FortiNET WLC instances '
            'successful.'
        )

        try:
            self.poll_wlcs()
            self.parse_metrics()
        except Exception as e:
            print(e)
            fortiwlc_up.add_metric([], 0)
        else:
            fortiwlc_up.add_metric([], 1)

        for key, ap_labels in self.ap_labels.items():
            labels = ap_labels.values()
            client_count = self.clients.get(key, 0)
            fortiwlc_clients.add_metric(
                labels,
                client_count
            )

        yield fortiwlc_clients
        yield fortiwlc_up

    def poll_wlcs(self):
        """ Polls all data from all WLCs APIs """
        for wlc in self.wlcs:
            wlc.poll()

    def parse_metrics(self):
        """ Parses collected WLC data """
        self.parse_by_ap()
        self.parse_by_ssid()

    def parse_by_ap(self):
        """ Generates labels for each AP/radio/SSID combo """
        self.ap_labels = {}
        for wlc in self.wlcs:
            for ap_data in wlc.managed_ap:
                model, campus, profile = ap_profile_string(ap_data)
                for radio_data in ap_data['radio']:
                    if radio_data['mode'] == 'Not Exist':
                        continue
                    
                    wifi_networks = self.get_wifi_networks(radio_data, wlc)
                    for wifi_network in wifi_networks:
                        key = (
                            wlc.name,
                            ap_data['name'],
                            str(radio_data['radio_id']),
                            wifi_network['name'],
                        )
                        self.ap_labels[key] = OrderedDict([
                            ('wlc', wlc.name),
                            ('ap_name', ap_data['name']),
                            ('ap_status', ap_data['status']),
                            ('ap_state', ap_data['state']),
                            ('profile', profile),
                            ('model', model),
                            ('radio_id', str(radio_data['radio_id'])),
                            ('campus', campus),
                            ('wifi_network', wifi_network['name']),
                            ('ssid', wifi_network['ssid']),
                        ])
                    if not wifi_networks:
                        key = (
                            wlc.name,
                            ap_data['name'],
                            str(radio_data['radio_id']),
                        )
                        self.ap_labels[key] = OrderedDict([
                            ('wlc', wlc.name),
                            ('ap_name', ap_data['name']),
                            ('ap_status', ap_data['status']),
                            ('ap_state', ap_data['state']),
                            ('profile', profile),
                            ('model', model),
                            ('radio_id', str(radio_data['radio_id'])),
                        ])
                        if campus:
                            self.ap_labels[key]['campus'] = campus

    def parse_by_ssid(self):
        """ Counts clients on each AP/radio/SSID combo """
        self.clients = defaultdict(int)
        for wlc in self.wlcs:
            for client in wlc.clients:
                key = (
                    wlc.name,
                    client['wtp_name'],
                    str(client['wtp_radio']),
                    client['vap_name'],
                )
                self.clients[key] += 1





    def get_wifi_networks(self, radio, wlc):
        wifi_networks = []
        for ssid_key in radio['ssid'].keys():
            try:
                group = next(filter(
                    lambda g: g['name'] == ssid_key,
                    wlc.vap_group
                ))
            except StopIteration:
                wifi_networks.append(self.parse_wifi_name(ssid_key))
            else:
                for vap_data in group['vaps']:
                    wifi_networks.append(
                        self.parse_wifi_name(vap_data['name'])
                    )
        return wifi_networks

    def parse_wifi_name(self, wifi_name):
        return {
            'name': wifi_name,
            'ssid': wifi_name.split('_')[-1],
        }
