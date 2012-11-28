"""Data Proxy - CSV dataconverteration adapter"""
import json
from StringIO import StringIO
from messytables import (
    CSVTableSet,
    headers_guess,
    headers_processor,
    offset_processor)
import requests
import base


class CSVConverter(base.Converter):

    def convert(self):

        table_set = CSVTableSet.from_fileobj(self.stream)
        row_set = table_set.tables.pop()
        offset, headers = headers_guess(row_set.sample)

        fields = []
        dup_columns = {}
        noname_count = 1
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
            fields.append(field_dict)
        row_set.register_processor(headers_processor([x['id'] for x in fields]))
        row_set.register_processor(offset_processor(offset + 1))

        data_row = {}
        result = []
        for row in row_set:
            for index, cell in enumerate(row):
                data_row[cell.column] = cell.value
            result.append(data_row)
        return fields, result
