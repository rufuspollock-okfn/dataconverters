import sys
from nose.tools import assert_equal
import dataconverters.arff as arff
from StringIO import StringIO

import difflib

class TestWrite:

    def test_1(self):
        metadata = {
            'fields': [
                {'type': 'Integer', 'id': u'temperature'}, 
                {'type': 'String', 'id': u'place'}
             ]
        }        
        records = [ 
            {'place': u'Cairo', 'temperature': 32}, 
            {'place': u'Alexandria', 'temperature': 22}, 
            {'place': u'Aswan', 'temperature': 42}, 
        ]
        
        desired_results = """@RELATION dataset\n
@ATTRIBUTE temperature NUMERIC
@ATTRIBUTE place STRING\n
@DATA\n32,'Cairo'
22,'Alexandria'
42,'Aswan'
"""
        out = StringIO()
        arff.write(out, records, metadata)
        out.seek(0)
        result = out.read()
                        
        assert_equal(result, desired_results)

