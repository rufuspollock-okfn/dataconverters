"""Data Proxy - CSV transformation adapter"""
from datetime import datetime
import json
from StringIO import StringIO
from tempfile import TemporaryFile
from messytables import (
    XLSTableSet,
    headers_guess,
    headers_processor,
    offset_processor)
import requests
import base


class XLSTransformer(base.Transformer):

    def transform(self):
        xlsdata = requests.get(self.url)
        handle = StringIO(xlsdata.content)
        with TemporaryFile() as xlsfile:
            xlsfile.write(handle.getvalue())
            table_set = XLSTableSet.from_fileobj(handle)
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
