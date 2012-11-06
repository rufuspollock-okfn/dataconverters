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
        assert ('"headers": ["date", "temperature", "place"]' in res.data)
        assert ('{"date": "2011-01-03", "place": "Berkeley", "temperature": '
                '"5"}' in res.data)

    def test_3_unicode_csv(self):
        """Test converting a CSV with unicode chars to JSON"""
        res = self.app.get('/api/convert/json?url='
                           'http://resources.opendatalabs.org/u/nigelb/'
                           'data-converters/csv/spanish_chars.csv')
        assert ('"headers": ["GF_ID", "FN_ID", "SF_ID", "GF", "F", "SF", '
                '"Gasto total 2011", "Descripci\u00f3n"]' in res.data)
        assert ('{"Gasto total 2011": "", "F": "", "Descripci\u00f3n": "", '
                '"SF_ID": "", "GF_ID": "Fuente: Presupuesto de Egresos de la '
                'Federaci\u00f3n 2011 An\u00e1lisis de las Funciones y '
                'Subfunciones del Gasto Programable por Destino del Gasto '
                '(neto) y Manual de Programaci\u00f3n y Presupuesto 2011 '
                'Anexo 11 Cat\u00e1logo Funcional ", "GF": "", "FN_ID": '
                '"", "SF": ""}' in res.data)

    def test_2_convert_csv(self):
        """Test converting a CSV with empty header to JSON"""
        res = self.app.get('/api/convert/json?url='
                           'http://resources.opendatalabs.org/u/nigelb/'
                           'data-converters/csv/simple_with_empty_title.csv')
        assert ('"headers": ["date", "column_1", "temperature", "place"]' in
                res.data)
        assert ('{{"date": "2011-01-03", "place": "Berkeley", "temperature": '
                '"5", "column_1": ""}' in res.data)
