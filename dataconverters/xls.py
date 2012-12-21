"""Data Proxy - CSV dataconversion adapter"""
from datetime import datetime
import json
from StringIO import StringIO
from tempfile import TemporaryFile
from messytables import (
    XLSTableSet,
    XLSXTableSet,
    headers_guess,
    headers_processor,
    offset_processor,
    type_guess,
    StringType,
    IntegerType,
    FloatType,
    DecimalType)
from messytables.types import DateUtilType


def xls_parse(stream, excel_type='xls', worksheet=1, header_type=0):
    '''Parse Excel (xls or xlsx) to structured objects.

    :param excel_type: xls | xlsx
    :param worksheet: index of worksheet to convert (starting from index = 1)
    '''
    sheet_number = int(worksheet) - 1

    xlsclass = XLSTableSet
    if excel_type == 'xlsx':
        xlsclass = XLSXTableSet
    table_set = xlsclass.from_fileobj(stream)
    try:
        row_set = table_set.tables[sheet_number]
    except IndexError:
        raise Exception('This file does not have worksheet number %d' % (self.sheet_number + 1))
    offset, headers = headers_guess(row_set.sample)

    fields = []
    dup_columns = {}
    noname_count = 1
    header_type = int(header_type)
    if header_type:
        guess_types = [StringType, IntegerType, FloatType, DecimalType, DateUtilType]
        row_types = type_guess(row_set.sample, guess_types)
    for index, field in enumerate(headers):
        field_dict = {}
        if "" == field:
            field = '_'.join(['column', str(noname_count)])
            headers[index] = field
            noname_count += 1
        if headers.count(field) == 1:
            field_dict['id'] = field
        else:
            dup_columns[field] = dup_columns.get(field, 0) + 1
            field_dict['id'] =  u'_'.join([field, str(dup_columns[field])])
        if header_type:
            if isinstance(row_types[index], DateUtilType):
                field_dict['type'] = 'DateTime'
            else:
                field_dict['type'] = str(row_types[index])
        fields.append(field_dict)
    row_set.register_processor(headers_processor([x['id'] for x in fields]))
    row_set.register_processor(offset_processor(offset + 1))

    info = {}
    result = []
    def row_iterator():
        for row in row_set:
            data_row = {}
            for index, cell in enumerate(row):
                data_row[cell.column] = cell.value
            yield data_row

    for row in row_set:
        for index, cell in enumerate(row):
            if isinstance(cell.value, datetime):
                info[cell.column] = cell.value.isoformat()
            else:
                info[cell.column] = cell.value
        result.append(info)
    return result, {'fields': fields}


def xlsx_parse(stream, worksheet=1):
    '''Convert from xlsx to JSON'''
    return xls_parse(stream, excel_type='xlsx', worksheet=worksheet)

