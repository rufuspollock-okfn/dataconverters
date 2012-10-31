import os
from collections import namedtuple
from mock import patch
from unittest2 import TestCase
from manhunter import app


FakeRequest = namedtuple('FakeRequest', ['text', 'status_code', 'headers'])


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

    @patch('manhunter.views.requests.get')
    def test_2_convert_csv(self, Mock):
        """Test converting a CSV to JSON"""
        csv_file = FakeRequest('Foo,Bar,priority_0\n1,2,3\n4,5,6', 200,
                                 {'content-type': 'text/plain'})
        Mock.return_value = csv_file
        res = self.app.get('/api/convert/json?url=http://example.csv')
        self.assertEqual('[{"Foo": "1", "Bar": "2", "priority_0": "3"}, '
                         '{"Foo": "4", "Bar": "5", "priority_0": "6"}]',
                         res.data)
