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
        iterator, metadata = xls.xls_parse(xlsfo)
        assert_equal([{"id": u"date"}, {"id": u"temperature"}, {"id":
                         u"place"}], metadata['fields'])
        content = [row for row in iterator]
        assert ({u'date': datetime.datetime(2011, 1, 1, 0, 0), u'place': u'Galway',
                u'temperature': 1.0} in content)

    def test_3_header_type(self):
        """Test guessing header type"""
        xlsfo = open(os.path.join(self.testdata_path, 'simple.xls'))
        iterator, metadata = xls.xls_parse(xlsfo, header_type=1)
        assert_equal([{'type': 'String', 'id': u'date'}, {'id':
                         u'temperature', 'type': 'Integer'}, {'id': u'place',
                         'type': 'String'}], metadata['fields'])

"""
    def test_2_convert_xlsx(self):
        ""Test converting a XLSX to JSON""
        res = self.app.get('/api/convert/json?url='
                           'http://resources.opendatalabs.org/u/nigelb/'
                           'data-converters/xls/simple.xlsx&type=xls&excel_type=xlsx')
        assert ('"metadata['fields']": [{"id": "date"}, {"id": "temperature"}, {"id": '
                '"place"}]' in res.data)
        assert ('{"date": "2011-01-03T00:00:00", "place": "Berkeley", '
                '"temperature": 5}' in res.data) """
