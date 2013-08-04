import json
import os
from subprocess import Popen
import tempfile


def parse(stream, **kwargs):
    '''
    Parse KML file and return python list and metadata.
    '''
    # Get a temporary file
    o = tempfile.NamedTemporaryFile()
    o.close()
    with tempfile.NamedTemporaryFile() as i:
        i.write(stream.read())

        i.flush()

        cmd = ['ogr2ogr', '-f', 'GeoJSON', o.name, i.name]
        inst = Popen(cmd)
        inst.communicate()

        stream = open(o.name, 'r')
        stream.seek(0)
        streamcontent = stream.read()
        stream.close()
        os.remove(o.name)

        decodedcontent = json.loads(streamcontent)

        return decodedcontent, {}

