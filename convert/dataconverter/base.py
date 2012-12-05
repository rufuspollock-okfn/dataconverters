dataconverters = {}
mime_types = {}


def register_dataconverter(converter):
    dataconverters[converter.get('name')] = converter
    for mime_type in converter.get('mime_types'):
        mime_types[mime_type] = converter


def find_dataconverter(converter_type=None, mime_type=None):

    def return_converter(info, error):
        if info:
            return info['class']
        else:
            raise Exception(error)

    if converter_type:
        info = dataconverters.get(converter_type, None)
        return return_converter(info, "No converter for type %s" % converter_type)
    if mime_type:
        info = mime_types.get(mime_type, None)
        return return_converter(info, "No converter for mime_type %s" % mime_type)
    raise Exception("No type specified")


def dataconverter(stream, metadata):
    """Get dataconverteration module for resource of given type"""

    trans_class = find_dataconverter(converter_type=metadata.get('type'),
                                     mime_type=metadata.get('mime_type'))
    return trans_class(stream, metadata)


class Converter(object):
    """Data resource dataconverter - abstract ckass"""

    def __init__(self, stream, metadata):
        self.stream = stream
        self.metadata = metadata
