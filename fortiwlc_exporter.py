import requests
import json
import time
import sys
from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY
from prometheus_client import Gauge
from exporter_functions_new import main


ssidapi = ['https://wlc1.anso.arnes.si/api/v2/cmdb/wireless-controller/vap-group/?vdom=root&access_token=kQ0bg3jg6pfn19kr4GdgzGx41dmk9w',
            'https://wlc2.anso.arnes.si/api/v2/cmdb/wireless-controller/vap-group/?vdom=root&access_token=9dprpq3xs8bxwGs10w03N5N9bt6dpp',
            'https://wlc3.anso.arnes.si/api/v2/cmdb/wireless-controller/vap-group/?vdom=root&access_token=60dzxQ3wNb1GbjjshryQ000NwN3yyj',
            'https://wlc4.anso.arnes.si/api/v2/cmdb/wireless-controller/vap-group/?vdom=root&access_token=wGzjNw1pQg5snmxp6m1jphQ94n41mw']

#test source api
testing = ['https://wlc.ansoext.arnes.si/api/v2/monitor/wifi/managed_ap/select/?vdom=root&access_token=r8g1y84z1q73x96s91gQq0pfGNd4x7']

#production source api
production = ['https://wlc1.anso.arnes.si/api/v2/monitor/wifi/managed_ap/select/?vdom=root&access_token=kQ0bg3jg6pfn19kr4GdgzGx41dmk9w',
          'https://wlc2.anso.arnes.si/api/v2/monitor/wifi/managed_ap/select/?vdom=root&access_token=9dprpq3xs8bxwGs10w03N5N9bt6dpp',
          'https://wlc3.anso.arnes.si/api/v2/monitor/wifi/managed_ap/select/?vdom=root&access_token=60dzxQ3wNb1GbjjshryQ000NwN3yyj',
          'https://wlc4.anso.arnes.si/api/v2/monitor/wifi/managed_ap/select/?vdom=root&access_token=wGzjNw1pQg5snmxp6m1jphQ94n41mw']

wlcarray = sys.argv[1]

#print(json.dumps(main(ssidapi,wlcarray), indent=4, sort_keys=True))


class FortiwlcCollector(object):
    def collect(self):
        client_count = GaugeMetricFamily('client_count','help',labels=['ap_name','campus_name','profile_name','model','wlc','status','state'])

        for ap_name, ap_data in main(ssidapi,wlcarray)['ap'].items():
            client_count.add_metric([ap_name,ap_data['campus_name'],ap_data['profile_name'],ap_data['model'],ap_data['wlc'],ap_data['status'],ap_data['state']], ap_data['client_count'])

        yield client_count

        '''client_count = GaugeMetricFamily('ap_client_count','help',labels=['ap_name'])
        ssid_count = GaugeMetricFamily('ssid_count','help',labels=['ap_name'])'''

        '''for campus_name, campus_data in main(ssidapi,production)['campus'].items():
            #print(campus_data)
            ap_count.add_metric([campus_name+' total'], campus_data['ap_count']['total'])
            ap_count.add_metric([campus_name+' reeboot_last_day'], campus_data['ap_count']['reboot_last_day'])
            ap_count.add_metric([campus_name+' connected'], campus_data['ap_count']['status']['connected'])
            ap_count.add_metric([campus_name+' disconnected'], campus_data['ap_count']['status']['disconnected'])
            ap_count.add_metric([campus_name+' authorized'], campus_data['ap_count']['status']['authorized'])
            ap_count.add_metric([campus_name+' discovered'], campus_data['ap_count']['status']['discovered'])
            ap_count.add_metric([campus_name+' model FAP221E'], campus_data['ap_count']['per_model'].get('FAP221E'))


        for wlc_name, wlc_data in main(ssidapi,production)['wlc'].items():
            ap_count.labels(wlc_name=wlc_name, wlc_label='wlc_slug').set(wlc_data['ap_count']['total'])
            ap_count.add_metric([wlc_name+' reboot_last_day'], wlc_data['ap_count']['reboot_last_day'])
            ap_count.add_metric([wlc_name+' connected'], wlc_data['ap_count']['status']['connected'])
            ap_count.add_metric([wlc_name+' disconnected'], wlc_data['ap_count']['status']['disconnected'])
            ap_count.add_metric([wlc_name+' authorized'], wlc_data['ap_count']['status']['authorized'])
            ap_count.add_metric([wlc_name+' discovered'], wlc_data['ap_count']['status']['discovered'])

'''
        '''for ap_name,ap_data in main(ssidapi,production)['ap'].items():
            ap_client_count.add_metric([ap_name], ap_data['client_count'])
            ssid_count.add_metric([ap_name], ap_data['ssid_count'])
            radio1_count.add_metric([ap_name], ap_data['per_radio']['1'])
            radio2_count.add_metric([ap_name], ap_data['per_radio']['2'])

        yield ap_client_count
        yield ssid_count
        yield radio1_count
        yield radio2_count


        campus_client_count = GaugeMetricFamily('campus_client_count','help',labels=['campus_name'])
        for campus_name,campus_data in main(ssidapi,production)['campus'].items():
            campus_client_count.add_metric([campus_name], campus_data['client_count'])

        yield campus_client_count'''


if __name__ == "__main__":
    REGISTRY.register(FortiwlcCollector())
    start_http_server(9118)
    while True: time.sleep(1)
