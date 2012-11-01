import os
from collections import namedtuple
from mock import patch
from unittest2 import TestCase
from manhunter import app


class TestCase(TestCase):

    def setUp(self):
        self.app = app.test_client()
        here = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.dirname(os.path.dirname(here))
        app.config.from_pyfile(os.path.join(config_path, 'settings.py'))
        app.config.from_pyfile(os.path.join(config_path, 'test_settings.py'),
                               silent=True)

    def test_1_convert_params(self):
        """Test not enough parameters to convert endpoint"""
        res = self.app.get('/convert/foo')
        self.assertEqual(404, res.status_code)

    def test_2_convert_csv(self):
        """Test converting a CSV to JSON"""
        res = self.app.get('/api/convert/json?url='
                           'http://resources.opendatalabs.org/u/nigelb/'
                           'data-converters/csv/simple.csv')
        #"headers": ["date", "temperature", "place"]
        assert ('"headers": ["date", "temperature", "place"]' in res.data)
        assert ('{"date": "2011-01-03", "place": "Berkeley", "temperature": '
                '"5"}' in res.data)
