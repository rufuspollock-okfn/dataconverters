import fiona


def parse(path, **kwargs):
    return fiona.collection(path), {}
