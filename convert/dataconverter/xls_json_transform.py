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
    offset_processor)
import requests
import base


class XLSConverter(base.Transformer):

    def __init__(self, url, query):
        super(XLSConverter, self).__init__(url, query)

        self.excel_type = self.query.get('excel_type', 'xls')
        self.sheet_number = int(self.query.get('worksheet', 1)) - 1

    def dataconverter(self):
        xlsdata = requests.get(self.url)
        mimetype = xlsdata.headers['content-type']
        if 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' == mimetype or 'xlsx' == self.excel_type:
            xlsclass = XLSXTableSet
        else:
            xlsclass = XLSTableSet
        handle = StringIO(xlsdata.content)
        with TemporaryFile() as xlsfile:
            xlsfile.write(handle.getvalue())
            table_set = xlsclass.from_fileobj(handle)
            try:
                row_set = table_set.tables[self.sheet_number]
            except IndexError:
                raise Exception('This file does not have worksheet number %d' % (self.sheet_number + 1))
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

            info = {}
            result = []
            for row in row_set:
                for index, cell in enumerate(row):
                    if isinstance(cell.value, datetime):
                        info[cell.column] = cell.value.isoformat()
                    else:
                        info[cell.column] = cell.value
                result.append(info)
            result_data = {'headers': fields, 'data': result}
            result_json = json.dumps(result_data)
            return result_json
