dataconverters = {}


def register_dataconverter(converter):
    dataconverters[converter.get('name')] = converter


def find_dataconverter(converter_type=None):
    if converter_type:
        info = dataconverters.get(converter_type, None)
        if info:
            return info['class']
        else:
            raise Exception("No converter for type %s" % force_type)
    raise Exception("No type specified")


def dataconverter(stream, metadata):
    """Get dataconverteration module for resource of given type"""

    trans_class = find_dataconverter(converter_type=metadata.get('type'))
    return trans_class(stream, metadata)


class Converter(object):
    """Data resource dataconverter - abstract ckass"""

    def __init__(self, stream, metadata):
        self.stream = stream
        self.metadata = metadata
