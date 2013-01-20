import json
import datetime
import decimal

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)


def write(stream, records, metadata, indent=2, **kwargs):
    '''Write records and metadata to JSON structure on the given stream
    
    :param stream: file-like object supporting writing.

    :return: null
    '''
    data = {
        'metadata': metadata,
        'records': [r for r in records]
        }
    json.dump(data, stream, indent=indent, cls=JSONEncoder)

