import datetime
import os
from nose.tools import assert_equal
import dataconverters.xls as xls

class TestParse:

    def setUp(self):
        here = os.path.dirname(os.path.abspath(__file__))
        testdata_path = os.path.dirname(here)
        self.testdata_path = os.path.join(testdata_path, 'testdata', 'xls')

    def test_1_convert_xls(self):
        """Test converting a XLS to JSON"""
        xlsfo = open(os.path.join(self.testdata_path, 'simple.xls'))
        iterator, metadata = xls.xls_parse(xlsfo, guess_types=False)
        assert_equal([{"id": u"date"}, {"id": u"temperature"}, {"id":
                         u"place"}], metadata['fields'])
        content = [row for row in iterator]
        assert ({u'date': datetime.datetime(2011, 1, 1, 0, 0), u'place': u'Galway',
                u'temperature': 1.0} in content)

    def test_2_header_type(self):
        """Test guessing header type"""
        xlsfo = open(os.path.join(self.testdata_path, 'simple.xls'))
        iterator, metadata = xls.xls_parse(xlsfo)
        assert_equal([{'type': 'String', 'id': u'date'}, {'id':
                         u'temperature', 'type': 'Integer'}, {'id': u'place',
                         'type': 'String'}], metadata['fields'])

    def test_3_convert_xlsx(self):
        """Test converting a XLSX to JSON"""
        xlsfo = open(os.path.join(self.testdata_path, 'simple.xlsx'))
        iterator, metadata = xls.xlsx_parse(xlsfo)
        assert_equal([{'type': 'String', 'id': u'date'}, {'id':
                         u'temperature', 'type': 'Integer'}, {'id': u'place',
                         'type': 'String'}], metadata['fields'])
        content = [row for row in iterator]
        assert ({u'date': datetime.datetime(2011, 1, 1, 0, 0), u'place': u'Galway',
                u'temperature': 1} in content)
