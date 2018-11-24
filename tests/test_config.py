import unittest
from copy import deepcopy
from io import StringIO

from fortiwlc_exporter.config import get_config, DEFAULTS


class TestConfigParser(unittest.TestCase):
    def test_config_empty(self):
        ''' Empty configuration provided '''
        config_file = StringIO('')
        expected_config = deepcopy(DEFAULTS)
        expected_config['wlcs'] = []
        config = get_config(config_file)
        self.assertEqual(config, expected_config)

    def test_config_main(self):
        ''' Only the main section provided - no wlcs '''
        config_file = StringIO('''
        [main]
        port=1234
        ''')
        expected_config = deepcopy(DEFAULTS)
        expected_config['wlcs'] = []
        expected_config['port'] = 1234
        config = get_config(config_file)
        self.assertEqual(config, expected_config)

    def test_config_wlcs(self):
        ''' Just wlcs provided - no main section '''
        config_file = StringIO('''
        [mywlc1]
        api_key=1234
        [mywlc2]
        user=a
        pass=b
        ''')
        expected_config = deepcopy(DEFAULTS)
        expected_config['wlcs'] = [
            {'name': 'mywlc1', 'api_key': '1234'},
            {'name': 'mywlc2', 'user': 'a', 'pass': 'b'}
        ]
        config = get_config(config_file)
        self.assertEqual(config, expected_config)
