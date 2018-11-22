import time
import sys
from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY
from fortiwlc_exporter.collector import FortiwlcCollector


WLCS = {
    'production': [
        ('wlc1.anso.arnes.si', 'kQ0bg3jg6pfn19kr4GdgzGx41dmk9w'),
        ('wlc2.anso.arnes.si', '9dprpq3xs8bxwGs10w03N5N9bt6dpp'),
        ('wlc3.anso.arnes.si', '60dzxQ3wNb1GbjjshryQ000NwN3yyj'),
        ('wlc4.anso.arnes.si', 'wGzjNw1pQg5snmxp6m1jphQ94n41mw'),
        ('wlc5.anso.arnes.si', '3696nbbws84k3078fnpzz3sN740zdc'),
        ('wlc6.anso.arnes.si', 'g50dd0m861fw7zdh7HdQ391nrg5f41'),
        ('wlc7.anso.arnes.si', 'y9Qksyrs3940ctfr9x7drdcss3n0dg'),
    ],
    'testing': [
        ('wlc.ansoext.arnes.si', 'r8g1y84z1q73x96s91gQq0pfGNd4x7'),
    ],
}


def start_server(group_name, port=9118):
    wlc_group = WLCS.get(group_name, [])
    REGISTRY.register(FortiwlcCollector(wlc_group))
    start_http_server(port)


def main():
    try:
        group_name = sys.argv[1]
    except IndexError:
        group_name = 'testing'
    start_server(group_name)
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
