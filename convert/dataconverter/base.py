import requests


dataconverterers = []


def register_dataconverterer(transformer):
    dataconverterers.append(transformer)


def find_dataconverterer(mime_type=None, force_type=None):
    info = None
    if force_type:
        for trans in dataconverterers:
            if force_type == trans["name"]:
                info = trans
        if info:
            return info['class']
        else:
            raise Exception("No dataconverterer for type %s" % force_type)

    if not mime_type:
        raise ValueError("Mime type should be specified")

    for trans in dataconverterers:
        if mime_type and mime_type in trans["mime_types"]:
            info = trans
    if not info:
        return None

    return info["class"]


def dataconverterer(url, query):
    """Get dataconverteration module for resource of given type"""

    r = requests.head(url)
    if not r.status_code == requests.codes.ok:
        raise Exception("Couldn't fetch the file from %s" % url)
    trans_class = find_dataconverterer(mime_type=r.headers['content-type'], force_type=query.get('type'))
    if not trans_class:
        raise Exception("No dataconverterer for type '%s'" % r.headers['content-type'])

    return trans_class(url, query)


class Converter(object):
    """Data resource dataconverterer - abstract ckass"""

    def __init__(self, url, query):
        self.url = url
        self.query = query
