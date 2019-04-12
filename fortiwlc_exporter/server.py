import logging
import urllib.parse as urlparse
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ForkingMixIn

from prometheus_client import CONTENT_TYPE_LATEST, CollectorRegistry, generate_latest
from prometheus_client.core import REGISTRY

from fortiwlc_exporter import settings
from fortiwlc_exporter.collector import FortiwlcCollector
from fortiwlc_exporter.exceptions import TimeoutError
from fortiwlc_exporter.utils import timeout


class ForkingHTTPServer(ForkingMixIn, HTTPServer):
    pass


class FortiwlcExporterHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        try:
            BaseHTTPRequestHandler.__init__(self, *args, **kwargs)
        except Exception as e:
            logging.exception('Failed to handle request: %s', e)

    @timeout()
    def collect(self, params):
        # de-dup target values
        hosts = set(params['target'])
        collector = FortiwlcCollector(hosts=hosts)
        if settings.NO_DEFAULT_COLLECTORS:
            registry = CollectorRegistry()
        else:
            registry = REGISTRY
        registry.register(collector)
        return generate_latest(registry)

    def do_GET(self):
        logging.info('Got request...')
        url = urlparse.urlparse(self.path)
        if url.path == '/probe':
            params = urlparse.parse_qs(url.query)
            if 'target' not in params:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Missing \'target\' from parameters')
                logging.error('Probe request missing target from parameters')
                return

            try:
                output = self.collect(params)
                self.send_response(200)
                self.send_header('Content-Type', CONTENT_TYPE_LATEST)
                self.end_headers()
                self.wfile.write(output)
                logging.info('Finished request.')
            except TimeoutError:
                logging.error('Collection timed out')
                self.send_response(408)
                self.end_headers()
                # self.wfile.write(traceback.format_exc())
            except Exception as e:
                logging.error('Internal error: %s', e)
                self.send_response(500)
                self.end_headers()
                # self.wfile.write(traceback.format_exc())

        elif url.path == '/':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(
                str.encode(
                    """<html>
            <head><title>FortiWLC Exporter</title></head>
            <body>
            <h1>FortiWLC Exporter</h1>
            <p>Visit <code>/probe?target=wlc.example.com</code> to use.</p>
            </body>
            </html>"""
                )
            )
        else:
            self.send_response(404)
            self.end_headers()

    def log_request(self, *args, **kwargs):
        pass


def start_server():
    logging.info('Listening on port :{}...'.format(settings.EXPORTER_PORT))
    server = ForkingHTTPServer(('', settings.EXPORTER_PORT), FortiwlcExporterHandler)
    server.serve_forever()
