"""Data Proxy - CSV dataconversion adapter"""
from datetime import date, datetime
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


def parse(stream, excel_type='xls', sheet=1, guess_types=True,
        strict_type_guess=False, encoding=None):
    '''Parse Excel (xls or xlsx) to structured objects.

    :param excel_type: xls | xlsx
    :param sheet: index of sheet in spreadsheet to convert (starting from index = 1)
    '''
    sheet_number = int(sheet) - 1

    xlsclass = XLSTableSet
    kwargs = { 'encoding': encoding }
    if excel_type == 'xlsx':
        xlsclass = XLSXTableSet
        # xlsx parser does not support encoding
        kwargs = {}
    table_set = xlsclass(stream, **kwargs)
    try:
        row_set = table_set.tables[sheet_number]
    except IndexError:
        raise Exception('This file does not have sheet number %d' %
                        (sheet_number + 1))
    offset, headers = headers_guess(row_set.sample)

    fields = []
    dup_columns = {}
    noname_count = 1
    if guess_types:
        guess_types = [StringType, IntegerType, FloatType, DecimalType,
                       DateUtilType]
        sample = row_set.sample
        for _ in range(offset + 1):
            sample.next()
        row_types = type_guess(sample, guess_types,
                               strict=strict_type_guess)
    for index, field in enumerate(headers):
        if isinstance(field, datetime) or isinstance(field, date):
            field = field.isoformat()
        field_dict = {}
        if "" == field:
            field = '_'.join(['column', str(noname_count)])
            headers[index] = field
            noname_count += 1
        if headers.count(field) == 1:
            field_dict['id'] = field
        else:
            dup_columns[field] = dup_columns.get(field, 0) + 1
            field_dict['id'] = u'_'.join([str(field), str(dup_columns[field])])
        if guess_types:
            if isinstance(row_types[index], DateUtilType):
                field_dict['type'] = 'DateTime'
            else:
                field_dict['type'] = str(row_types[index])
        fields.append(field_dict)
    row_set.register_processor(headers_processor([x['id'] for x in fields]))
    row_set.register_processor(offset_processor(offset + 1))

    def row_iterator():
        for row in row_set:
            data_row = {}
            for index, cell in enumerate(row):
                data_row[cell.column] = cell.value
            yield data_row

    return row_iterator(), {'fields': fields}
