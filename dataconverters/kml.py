import json
import os
from subprocess import Popen
import tempfile


def parse(stream, **kwargs):
    '''Parse KML file and return row iterator plus metadata.
    '''
    # Get a temporary file
    o = tempfile.NamedTemporaryFile()
    o.close()
    with tempfile.NamedTemporaryFile() as i:
        # Write kml stream into input file
        i.write(stream.read())

        # Flush to disk
        i.flush()

        # Perform conversion with ogr2ogr
        cmd = ['ogr2ogr', '-f', 'GeoJSON', o.name, i.name]
        inst = Popen(cmd)
        stdout, stderr = inst.communicate()

        # Read the output
        stream = open(o.name, 'r')
        stream.seek(0)
        streamcontent = stream.readlines()
        stream.close()
        os.remove(o.name)

        # Convert the stream to python
        content = ''.join(streamcontent)
        decodedcontent = json.loads(content)

        return decodedcontent

