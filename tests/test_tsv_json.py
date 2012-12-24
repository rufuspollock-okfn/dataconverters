import os
import datetime
from nose.tools import assert_equal
import dataconverters.csv as csvconvert


class TestParse:

    def setUp(self):
        here = os.path.dirname(os.path.abspath(__file__))
        testdata_path = os.path.dirname(here)
        self.testdata_path = os.path.join(testdata_path, 'testdata', 'tsv')

    def test_1_convert_csv(self):
        """Test converting a CSV to JSON"""
        csv = open(os.path.join(self.testdata_path, 'simple.tsv'))
        iterator, metadata = csvconvert.parse(csv, delimiter='\t', guess_types=False)
        assert_equal(
            [{'id': u'date'}, {'id': u'temperature'}, {'id': u'place'}],
            metadata['fields'])
        rows = [ row for row in iterator ]
        assert_equal(len(rows), 6)
        assert ({u'date': u'2011-01-03', u'place': u'Berkeley', u'temperature':
            u'5'} in rows)
