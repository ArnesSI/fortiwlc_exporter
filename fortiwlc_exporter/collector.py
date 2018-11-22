from prometheus_client.core import GaugeMetricFamily

from .exporter_functions_new import main


class FortiwlcCollector:
    def __init__(self, ssidapi, wlcarray):
        self.ssidapi = ssidapi
        self.wlcarray = wlcarray

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
            wlc_data = main(self.ssidapi, self.wlcarray)

            for ap_name, ap_data in wlc_data['ap'].items():
                fortiwlc_clients_by_ap.add_metric(
                    [
                        ap_name,
                        ap_data['campus_name'],
                        ap_data['profile_name'],
                        ap_data['model'],
                        ap_data['wlc'],
                        ap_data['status'],
                        ap_data['state']
                    ],
                    ap_data['client_count']
                )

        except:
            fortiwlc_up.add_metric([], 0)

        else:
            fortiwlc_up.add_metric([], 1)

        yield fortiwlc_clients_by_ap
        yield fortiwlc_up
