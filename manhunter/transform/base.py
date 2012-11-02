import requests


transformers = []


def register_transformer(transformer):
    transformers.append(transformer)


def find_transformer(mime_type=None, force_type=None):
    if force_type:
        for trans in transformers:
            if force_type == trans["name"]:
                info = trans
        return info["class"]

    if not mime_type:
        raise ValueError("Mime type should be specified")

    info = None
    for trans in transformers:
        if mime_type and mime_type in trans["mime_types"]:
            info = trans
    if not info:
        return None

    return info["class"]


def transformer(url, query):
    """Get transformation module for resource of given type"""

    r = requests.head(url)
    if not r.status_code == requests.codes.ok:
        raise Exception("Couldn't fetch the file from %s" % url)
    trans_class = find_transformer(mime_type=r.headers['content-type'], force_type=query.get('type'))
    if not trans_class:
        raise Exception("No transformer for type '%s'" % r.headers['content-type'])

    return trans_class(url, query)


class Transformer(object):
    """Data resource transformer - abstract ckass"""

    def __init__(self, url, query):
        self.url = url
        self.query = query
