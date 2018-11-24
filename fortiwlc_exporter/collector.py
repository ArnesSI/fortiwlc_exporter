from prometheus_client.core import GaugeMetricFamily

from .parsers import parse_ap_data
from .fortiwlc import FortiWLC


class FortiwlcCollector:
    def __init__(self, config):
        self.config = config
        self.wlcs = self.init_wlcs()
        self.by_ap = {}

    def init_wlcs(self):
        """ Initializes FortiWLC instances """
        wlcs = []
        for wlc_params in self.config.get('wlcs', []):
            wlcs.append(FortiWLC(**wlc_params))
        return wlcs

    def collect(self):
        fortiwlc_clients_by_ap = GaugeMetricFamily(
            'fortiwlc_clients_by_ap',
            'Number of clients connected to a specific access point. '
            'Retrieved from wifi/managed_ap/select/ API endpoint.',
            labels=[
                'ap_name',
                'campus_name',
                'profile_name',
                'model',
                'wlc',
                'status',
                'state'
            ]
        )
        fortiwlc_up = GaugeMetricFamily(
            'fortiwlc_up',
            'Was the last scrape of data from all FortiNET WLC instances '
            'successful.'
        )

        try:
            self.poll_wlcs()
            self.parse_metrics()
        except Exception:
            fortiwlc_up.add_metric([], 0)
        else:
            fortiwlc_up.add_metric([], 1)

        for ap_data in self.by_ap.values():
            fortiwlc_clients_by_ap.add_metric(
                [
                    ap_data['name'],
                    ap_data['campus_name'],
                    ap_data['profile_name'],
                    ap_data['model'],
                    ap_data['wlc'],
                    ap_data['status'],
                    ap_data['state']
                ],
                ap_data['client_count']
            )

        yield fortiwlc_clients_by_ap
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
        """ Parses data from WLCs and generates info (dict) about each AP """
        self.by_ap = {}
        for wlc in self.wlcs:
            for ap_data in wlc.managed_ap:
                self.by_ap[ap_data['name']] = parse_ap_data(ap_data, wlc.name)

    def parse_by_ssid(self):
        # not yet implemented
        pass
