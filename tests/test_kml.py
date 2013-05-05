import os
from nose.tools import assert_equal
from dataconverters import kml

class TestParse:

    def setUp(self):
        here = os.path.dirname(os.path.abspath(__file__))
        testdata_path = os.path.dirname(here)
        self.testdata_path = os.path.join(testdata_path, 'testdata', 'kml')

    def test_1_convert_kml(self):
        kmlfile = open(os.path.join(self.testdata_path, 'AngolaTelecoms.kml'))
        output = kml.parse(kmlfile)
        assert_equal(u'FeatureCollection', output['type'])
        assert_equal(15, len(output['features']))
        assert_equal(u'Feature', output['features'][0]['type'])
        assert_equal(u'LineString', output['features'][0]['geometry']['type'])
        assert_equal(239,
                     len(output['features'][0]['geometry']['coordinates']))
