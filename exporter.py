import requests
import json
import time
import sys
from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY
from prometheus_client import Gauge
from fortiwlc_exporter.collector import FortiwlcCollector


ssidapi = [
    'https://wlc1.anso.arnes.si/api/v2/cmdb/wireless-controller/vap-group/?vdom=root&access_token=kQ0bg3jg6pfn19kr4GdgzGx41dmk9w',
    'https://wlc2.anso.arnes.si/api/v2/cmdb/wireless-controller/vap-group/?vdom=root&access_token=9dprpq3xs8bxwGs10w03N5N9bt6dpp',
    'https://wlc3.anso.arnes.si/api/v2/cmdb/wireless-controller/vap-group/?vdom=root&access_token=60dzxQ3wNb1GbjjshryQ000NwN3yyj',
    'https://wlc4.anso.arnes.si/api/v2/cmdb/wireless-controller/vap-group/?vdom=root&access_token=wGzjNw1pQg5snmxp6m1jphQ94n41mw',
    'https://wlc5.anso.arnes.si/api/v2/cmdb/wireless-controller/vap-group/?vdom=root&access_token=3696nbbws84k3078fnpzz3sN740zdc',
    'https://wlc6.anso.arnes.si/api/v2/cmdb/wireless-controller/vap-group/?vdom=root&access_token=g50dd0m861fw7zdh7HdQ391nrg5f41',
    'https://wlc7.anso.arnes.si/api/v2/cmdb/wireless-controller/vap-group/?vdom=root&access_token=y9Qksyrs3940ctfr9x7drdcss3n0dg',
]

#test source api
testing = ['https://wlc.ansoext.arnes.si/api/v2/monitor/wifi/managed_ap/select/?vdom=root&access_token=r8g1y84z1q73x96s91gQq0pfGNd4x7']

#production source api
production = [
    'https://wlc1.anso.arnes.si/api/v2/monitor/wifi/managed_ap/select/?vdom=root&access_token=kQ0bg3jg6pfn19kr4GdgzGx41dmk9w',
    'https://wlc2.anso.arnes.si/api/v2/monitor/wifi/managed_ap/select/?vdom=root&access_token=9dprpq3xs8bxwGs10w03N5N9bt6dpp',
    'https://wlc3.anso.arnes.si/api/v2/monitor/wifi/managed_ap/select/?vdom=root&access_token=60dzxQ3wNb1GbjjshryQ000NwN3yyj',
    'https://wlc4.anso.arnes.si/api/v2/monitor/wifi/managed_ap/select/?vdom=root&access_token=wGzjNw1pQg5snmxp6m1jphQ94n41mw',
    'https://wlc5.anso.arnes.si/api/v2/monitor/wifi/managed_ap/select/?vdom=root&access_token=3696nbbws84k3078fnpzz3sN740zdc',
    'https://wlc6.anso.arnes.si/api/v2/monitor/wifi/managed_ap/select/?vdom=root&access_token=g50dd0m861fw7zdh7HdQ391nrg5f41',
    'https://wlc7.anso.arnes.si/api/v2/monitor/wifi/managed_ap/select/?vdom=root&access_token=y9Qksyrs3940ctfr9x7drdcss3n0dg',
]

try:
    wlcarray = sys.argv[1]
except IndexError:
    wlcarray = 'testing'

#print(json.dumps(main(ssidapi,wlcarray), indent=4, sort_keys=True))


def start_server(port=9118):
    REGISTRY.register(FortiwlcCollector(ssidapi, wlcarray))
    start_http_server(port)


def main():
    start_server()
    while True: time.sleep(1)


if __name__ == "__main__":
    main()
