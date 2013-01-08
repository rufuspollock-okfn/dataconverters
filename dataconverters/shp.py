import fiona
import tempfile

def parse(path, **kwargs):
    return fiona.collection(path), {}
