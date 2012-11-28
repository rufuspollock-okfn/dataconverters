import os
from unittest import TestCase
from convert.dataconverter import dataconverter


class TestCase(TestCase):

    def setUp(self):
        here = os.path.dirname(os.path.abspath(__file__))
        testdata_path = os.path.dirname(os.path.dirname(os.path.dirname(here)))
        self.testdata_path = os.path.join(testdata_path, 'testdata', 'csv')

    def test_1_convert_csv(self):
        """Test converting a CSV to JSON"""
        csv = open(os.path.join(self.testdata_path, 'simple.csv'))
        data = dataconverter(csv, {'type': 'csv'})
        headers, content = data.convert()
        self.assertEqual([{'id': u'date'}, {'id': u'temperature'}, {'id': u'place'}], headers)
        assert ({u'date': u'2011-01-03', u'place': u'Berkeley', u'temperature': u'5'} in content)

    def test_2_unicode_csv(self):
        """Test converting a CSV with unicode chars to JSON"""
        csv = open(os.path.join(self.testdata_path, 'spanish_chars.csv'))
        data = dataconverter(csv, {'type': 'csv'})
        headers, content = data.convert()
        self.assertEqual([{"id": u"GF_ID"}, {"id": u"FN_ID"}, {"id": u"SF_ID"},
                {"id": u"GF"}, {"id": u"F"}, {"id": u"SF"}, {"id":
                u"Gasto total 2011"}, {"id": u"Descripci\u00f3n"}],
                headers)
        assert ({u"Gasto total 2011": u"", u"F": u"", u"Descripci\u00f3n": "",
                u"SF_ID": u"", u"GF_ID": u"Fuente: Presupuesto de Egresos de"
                u" la Federaci\u00f3n 2011 An\u00e1lisis de las Funciones y "
                u"Subfunciones del Gasto Programable por Destino del Gasto "
                u"(neto) y Manual de Programaci\u00f3n y Presupuesto 2011 "
                u"Anexo 11 Cat\u00e1logo Funcional ", u"GF": "", u"FN_ID":
                u"", u"SF": u""} in content)


    def test_4_empty_title_convert_csv(self):
        """Test converting a CSV with empty header to JSON"""
        csv = open(os.path.join(self.testdata_path, 'simple_empty_title.csv'))
        data = dataconverter(csv, {'type': 'csv'})
        headers, content = data.convert()
        self.assertEqual([{"id": u"date"}, {"id": u"column_1"}, {"id": u"temperature"}, {"id": u"place"}], headers)
        assert ({u"date": u"2011-01-03", u"place": u"Berkeley", u"temperature": u"5", u"column_1": u""} in content)
