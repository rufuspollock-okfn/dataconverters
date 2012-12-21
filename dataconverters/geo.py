import fiona
import tempfile

def shp_parse(path):
    # doees not work as we need *all* the files
    # temp = tempfile.NamedTemporaryFile(suffix='.shp')
    # temp.write(stream.read())
    return fiona.collection(path), {}

