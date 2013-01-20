import json
import datetime
import csv

from messytables import (
    CSVTableSet,
    headers_guess,
    headers_processor,
    offset_processor,
    types_processor,
    type_guess,
    StringType,
    IntegerType,
    FloatType,
    DecimalType)
from messytables.types import DateUtilType


def parse(stream, guess_types=True, **kwargs):
    '''Parse CSV file and return row iterator plus metadata (fields etc).

    Additional CSV arguments as per
    http://docs.python.org/2/library/csv.html#csv-fmt-params

    :param delimiter:
    :param quotechar: 

    There is also support for:

    :param encoding: file encoding (will be guess with chardet if not provided)


    You can process csv as well as tsv files using this function. For tsv just
    pass::

        delimiter='\t'
    '''
    metadata = dict(**kwargs)
    delimiter = metadata.get('delimiter', None)
    quotechar = metadata.get('quotechar', None)
    encoding = metadata.get('encoding', None)
    table_set = CSVTableSet.from_fileobj(stream, delimiter=delimiter,
            quotechar=quotechar, encoding=encoding)
    row_set = table_set.tables.pop()
    offset, headers = headers_guess(row_set.sample)

    fields = []
    dup_columns = {}
    noname_count = 1
    if guess_types:
        guessable_types = [StringType, IntegerType, FloatType, DecimalType,
                           DateUtilType]
        row_types = type_guess(row_set.sample, guessable_types)
    for index, field in enumerate(headers):
        field_dict = {}
        if "" == field:
            field = '_'.join(['column', unicode(noname_count)])
            headers[index] = field
            noname_count += 1
        if headers.count(field) == 1:
            field_dict['id'] = field
        else:
            dup_columns[field] = dup_columns.get(field, 0) + 1
            field_dict['id'] = u'_'.join([field, unicode(dup_columns[field])])
        if guess_types:
            if isinstance(row_types[index], DateUtilType):
                field_dict['type'] = 'DateTime'
            else:
                field_dict['type'] = str(row_types[index])
        fields.append(field_dict)
    row_set.register_processor(headers_processor([x['id'] for x in fields]))
    row_set.register_processor(offset_processor(offset + 1))
    if guess_types:
        row_set.register_processor(types_processor(row_types))

    def row_iterator():
        for row in row_set:
            data_row = {}
            for index, cell in enumerate(row):
                data_row[cell.column] = cell.value
            yield data_row
    return row_iterator(), {'fields': fields}


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()

        return json.JSONEncoder.default(self, obj)


def csv_to_json(stream, **kwargs):
    '''TODO: document output format'''
    iterator, metadata = parse(stream, **kwargs)
    # TODO: convert python types to json serializable stuff!
    # e.g. datetimes to isoformat strings etc
    out = json.dumps(
        {
            'metadata': metadata,
            'records': [row for row in iterator]
        },
        cls=DateEncoder)
    return out, metadata


def write(stream, records, metadata, **kwargs):
    '''Write records and metadata to CSV structure on the given stream
    
    :param stream: file-like object supporting writing.

    :param kwargs: passed directly through to the csv.DictWriter object

    :return: null
    '''
    fields = [ f['id'] for f in metadata['fields'] ]
    writer = csv.DictWriter(stream, fields, **kwargs)
    # TODO: possibly using writerows would be faster (??)
    writer.writeheader()
    for r in records:
        writer.writerow(r)

