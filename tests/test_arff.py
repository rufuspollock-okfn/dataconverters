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
        desired_results = """@RELATION dataset

@ATTRIBUTE temperature NUMERIC
@ATTRIBUTE place STRING

@DATA\n32,'Cairo'
22,'Alexandria'
42,'Aswan'
"""
        out = StringIO()
        arff.write(out, records, metadata)
        out.seek(0)
        result = out.read()
        print '####'
        print result
        print '####'
        print desired_results
        print '####'
        
        print '\n======Diff======\n'
        d = difflib.Differ()
        diff = list(d.compare(desired_results, result))
        print ''.join(diff)
        
        print zip(desired_results, result)
        
        print '\n======Diff======\n'
                
        assert_equal(result, desired_results)

