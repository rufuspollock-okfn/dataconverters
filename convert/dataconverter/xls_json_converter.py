"""Data Proxy - CSV dataconverteration adapter"""
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
import requests
import base


class XLSConverter(base.Converter):

    def __init__(self, stream, metadata):
        super(XLSConverter, self).__init__(stream, metadata)

        self.excel_type = self.metadata.get('excel_type', 'xls')
        self.sheet_number = int(self.metadata.get('worksheet', 1)) - 1
        self.xlsclass = XLSTableSet

    def convert(self):
        xlsclass = self.xlsclass
        if 'xlsx' == self.excel_type:
            xlsclass = XLSXTableSet
        table_set = xlsclass.from_fileobj(self.stream)
        try:
            row_set = table_set.tables[self.sheet_number]
        except IndexError:
            raise Exception('This file does not have worksheet number %d' % (self.sheet_number + 1))
        offset, headers = headers_guess(row_set.sample)

        fields = []
        dup_columns = {}
        noname_count = 1
        header_type = int(self.metadata.get('header_type', 0))
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
        for row in row_set:
            for index, cell in enumerate(row):
                if isinstance(cell.value, datetime):
                    info[cell.column] = cell.value.isoformat()
                else:
                    info[cell.column] = cell.value
            result.append(info)
        return fields, result


class XLSXConverter(XLSConverter):

    def __init__(self, stream, metadata):
        super(XLSXConverter, self).__init__(stream, metadata)

        self.xlsclass = XLSXTableSet
