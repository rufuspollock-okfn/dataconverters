transformers = []


def register_transformer(transformer):
    transformers.append(transformer)


def find_transformer(extension=None, mime_type=None):
    if not extension and not mime_type:
        raise ValueError("Either extension or mime type should be specified")

    info = None
    for trans in transformers:
        if extension and extension in trans["extensions"]:
            info = trans
        if mime_type and mime_type in trans["mime_types"]:
            info = trans
    if not info:
        return None

    return info["class"]


def transformer(type_name, url, query):
    """Get transformation module for resource of given type"""

    trans_class = find_transformer(extension=type_name)
    if not trans_class:
        raise Exception("No transformer for type '%s'" % type_name)

    return trans_class(url, query)


class Transformer(object):
    """Data resource transformer - abstract ckass"""

    def __init__(self, url, query):
        self.url = url
        self.query = query
