# -*- coding: utf-8
import os
import datetime
from nose.tools import assert_equal
import dataconverters.commas as csvconvert


class TestParse:

    def setUp(self):
        here = os.path.dirname(os.path.abspath(__file__))
        testdata_path = os.path.dirname(here)
        self.testdata_path = os.path.join(testdata_path, 'testdata', 'csv')

    def test_1_convert_csv(self):
        """Test converting a CSV to JSON"""
        csv = open(os.path.join(self.testdata_path, 'simple.csv'))
        iterator, metadata = csvconvert.parse(csv)
        assert_equal(
            [{'id': u'date', 'type': 'DateTime'}, {'id': u'temperature',
            'type': 'Integer'}, {'id': u'place', 'type': 'String'}],
            metadata['fields'])
        rows = [ row for row in iterator ]
        assert_equal(len(rows), 6)
        print rows
        assert ({u'date': datetime.datetime(2011, 1, 3, 0, 0),
                u'place': u'Berkeley', u'temperature': 5} in rows)

    def test_2_unicode_csv(self):
        """Test converting a CSV with unicode chars to JSON"""
        csv = open(os.path.join(self.testdata_path, 'spanish_chars.csv'))
        iterator, metadata = csvconvert.parse(csv, guess_types=False)
        assert_equal(
            [{"id": u"GF_ID"}, {"id": u"FN_ID"}, {"id": u"SF_ID"},
                {"id": u"GF"}, {"id": u"F"}, {"id": u"SF"},
                {"id": u"Gasto total 2011"}, {"id": u"Descripci\u00f3n"}],
            metadata['fields'])
        content = [row for row in iterator]
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
        iterator, metadata = csvconvert.parse(csv, guess_types=False)
        assert_equal([{"id": u"date"}, {"id": u"column_1"}, {"id":
            u"temperature"}, {"id": u"place"}],
            metadata['fields'])
        content = [row for row in iterator]
        assert ({u"date": u"2011-01-03", u"place": u"Berkeley", u"temperature": u"5", u"column_1": u""} in content)

    def test_5_header_type(self):
        """Test guessing header type"""
        csv = open(os.path.join(self.testdata_path, 'simple.csv'))
        iterator, metadata = csvconvert.parse(csv, header_type=1)
        assert_equal([{'type': 'DateTime', 'id': u'date'}, {'id':
                         u'temperature', 'type': 'Integer'}, {'id': u'place',
                         'type': 'String'}], metadata['fields'])
        rows = [ row for row in iterator ]
        assert_equal(len(rows), 6)
        assert_equal({u'date': datetime.datetime(2011, 1, 3), u'place': u'Berkeley', u'temperature':
            5}, rows[5])


import json
class TestCSVToJSON:
    def setUp(self):
        here = os.path.dirname(os.path.abspath(__file__))
        testdata_path = os.path.dirname(here)
        self.testdata_path = os.path.join(testdata_path, 'testdata', 'csv')

    def test_1_convert_csv(self):
        """Test converting a CSV to JSON"""
        csv = open(os.path.join(self.testdata_path, 'simple.csv'))
        thejson, metadata = csvconvert.csv_to_json(csv, guess_types=False)
        assert_equal(
            [{'id': u'date'}, {'id': u'temperature'}, {'id': u'place'}],
            metadata['fields'])
        data = json.loads(thejson)
        assert_equal(len(data['records']), 6)
        assert ({u'date': u'2011-01-03', u'place': u'Berkeley', u'temperature':
            u'5'} in data['records'])


from StringIO import StringIO
class TestWrite:

    def test_1(self):
        metadata = {
            'fields': [
                { 'id': 'A' },
                { 'id': 'B' }
            ]
        }
        records = [ {'A': u'☺', 'B': 2}, {'A': 2, 'B': 3} ]
        out = StringIO()
        csvconvert.write(out, records, metadata)
        out.seek(0)
        result = out.read()
        assert_equal(result, '''A,B\r\n☺,2\r\n2,3\r\n''')

