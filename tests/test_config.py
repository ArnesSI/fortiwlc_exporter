import unittest

from copy import deepcopy
from io import StringIO
from unittest.mock import MagicMock

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
        debug=yes
        password=abcd
        ''')
        expected_config = {}
        expected_config['wlcs'] = []
        expected_config['port'] = 1234
        expected_config['debug'] = True
        expected_config['workers'] = 2
        expected_config['username'] = ''
        expected_config['password'] = 'abcd'
        config = get_config(config_file)
        self.assertEqual(config, expected_config)

    def test_config_wlcs(self):
        ''' Just wlcs provided - no main section '''
        config_file = StringIO('''
        [mywlc1]
        api_key=1234
        [mywlc2]
        username=a
        password=b
        ''')
        expected_config = [
            {'name': 'mywlc1', 'api_key': '1234', 'username': '', 'password': ''},
            {'name': 'mywlc2', 'username': 'a', 'password': 'b'}
        ]
        config = get_config(config_file)
        self.assertEqual(config['wlcs'], expected_config)

    def test_config_extra(self):
        ''' Provide extra option that overrides config '''
        config_file = StringIO('''
        [main]
        port=1234
        debug=yes
        ''')
        extra = MagicMock(port=4321)
        config = get_config(config_file, extra=extra)
        self.assertEqual(config['port'], 4321)
        self.assertTrue(config['debug'])
