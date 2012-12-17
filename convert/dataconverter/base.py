dataconverters = {}
mime_types = {}


def register_dataconverter(converter):
    dataconverters[(converter.get('name'), converter.get('target'))] = converter
    for mime_type in converter.get('mime_types'):
        mime_types[(mime_type, converter.get('target'))] = converter


def find_dataconverter(converter_type=None, mime_type=None, target=None):

    def return_converter(info, error):
        if info:
            return info['class']
        else:
            raise Exception(error)

    if converter_type:
        info = dataconverters.get((converter_type, target), None)
        return return_converter(info, "No converter for '%s' to '%s'" % (converter_type, target))
    if mime_type:
        info = mime_types.get((mime_type, target), None)
        return return_converter(info, "No converter for mime_type '%s' to '%s'" % (mime_type, target))
    raise Exception("No type specified")


def dataconverter(stream, metadata):
    """Get dataconverteration module for resource of given type"""

    trans_class = find_dataconverter(converter_type=metadata.get('type'),
                                     mime_type=metadata.get('mime_type'),
                                     target=metadata.get('target'))
    return trans_class(stream, metadata)


class Converter(object):
    """Data resource dataconverter - abstract ckass"""

    def __init__(self, stream, metadata):
        self.stream = stream
        self.metadata = metadata
