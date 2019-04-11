import unittest
from copy import deepcopy
from io import StringIO
from unittest.mock import MagicMock

from fortiwlc_exporter import settings
from fortiwlc_exporter.exporter import parse_config_file


class TestConfigParser(unittest.TestCase):
    def setUp(self):
        self.orig_settings = {
            s: deepcopy(getattr(settings, s))
            for s in filter(lambda x: not x.startswith('__'), settings.__dict__.keys())
        }

    def tearDown(self):
        for k, v in self.orig_settings.items():
            setattr(settings, k, v)

    def test_config_empty(self):
        ''' Empty configuration provided '''
        config_file = StringIO('')
        expected_settings = {}
        expected_settings['WLCS'] = []
        expected_settings['EXPORTER_PORT'] = 9118
        expected_settings['DEBUG'] = False
        expected_settings['WORKERS'] = 1
        expected_settings['WLC_USERNAME'] = None
        expected_settings['WLC_PASSWORD'] = None
        expected_settings['WLC_API_KEY'] = None
        expected_settings['NO_DEFAULT_COLLECTORS'] = True
        expected_settings['ONE_OFF'] = False
        expected_settings['TIMEOUT'] = 60
        parse_config_file(config_file)
        new_settings = {
            s: deepcopy(getattr(settings, s))
            for s in filter(lambda x: not x.startswith('__'), settings.__dict__.keys())
        }
        self.assertDictEqual(new_settings, expected_settings)

    def test_config_main(self):
        ''' Only the main section provided - no wlcs '''
        config_file = StringIO(
            '''
        exporter_port: 1234
        wlc_password: abcd
        '''
        )
        expected_settings = {}
        expected_settings['WLCS'] = []
        expected_settings['EXPORTER_PORT'] = 1234
        expected_settings['DEBUG'] = False
        expected_settings['WORKERS'] = 1
        expected_settings['WLC_USERNAME'] = None
        expected_settings['WLC_PASSWORD'] = 'abcd'
        expected_settings['WLC_API_KEY'] = None
        expected_settings['NO_DEFAULT_COLLECTORS'] = True
        expected_settings['ONE_OFF'] = False
        expected_settings['TIMEOUT'] = 60
        parse_config_file(config_file)
        new_settings = {
            s: deepcopy(getattr(settings, s))
            for s in filter(lambda x: not x.startswith('__'), settings.__dict__.keys())
        }
        self.assertDictEqual(new_settings, expected_settings)

    def test_config_wlcs(self):
        ''' Just wlcs specified - no other settings '''
        config_file = StringIO(
            '''
        wlcs:
          - wlc1
          - wlc2
        '''
        )

        expected_settings = {}
        expected_settings['WLCS'] = ['wlc1', 'wlc2']
        expected_settings['EXPORTER_PORT'] = 9118
        expected_settings['DEBUG'] = False
        expected_settings['WORKERS'] = 1
        expected_settings['WLC_USERNAME'] = None
        expected_settings['WLC_PASSWORD'] = None
        expected_settings['WLC_API_KEY'] = None
        expected_settings['NO_DEFAULT_COLLECTORS'] = True
        expected_settings['ONE_OFF'] = False
        expected_settings['TIMEOUT'] = 60
        parse_config_file(config_file)
        new_settings = {
            s: deepcopy(getattr(settings, s))
            for s in filter(lambda x: not x.startswith('__'), settings.__dict__.keys())
        }
        self.assertEqual(new_settings, expected_settings)
