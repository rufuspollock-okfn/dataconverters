import os
from unittest import TestCase
from convert.dataconverter import dataconverter


class TestCase(TestCase):

    def setUp(self):
        here = os.path.dirname(os.path.abspath(__file__))
        testdata_path = os.path.dirname(os.path.dirname(os.path.dirname(here)))
        self.testdata_path = os.path.join(testdata_path, 'testdata', 'xls')

    def test_1_convert_xls(self):
        """Test converting a XLS to JSON"""
        xls = open(os.path.join(self.testdata_path, 'simple.xls'))
        data = dataconverter(xls, {'type': 'xls'})
        headers, content = data.convert()
        self.assertEqual([{"id": u"date"}, {"id": u"temperature"}, {"id":
                         u"place"}], headers)
        assert ({u"date": u"2011-01-03T00:00:00", u"place": u"Berkeley",
                "temperature": 5.0} in content)

"""
    def test_2_convert_xlsx(self):
        ""Test converting a XLSX to JSON""
        res = self.app.get('/api/convert/json?url='
                           'http://resources.opendatalabs.org/u/nigelb/'
                           'data-converters/xls/simple.xlsx&type=xls&excel_type=xlsx')
        assert ('"headers": [{"id": "date"}, {"id": "temperature"}, {"id": '
                '"place"}]' in res.data)
        assert ('{"date": "2011-01-03T00:00:00", "place": "Berkeley", '
                '"temperature": 5}' in res.data) """
