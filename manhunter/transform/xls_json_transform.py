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
            row_set.register_processor(headers_processor(headers))
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
            result_data = {'headers': headers, 'data': result}
            result_json = json.dumps(result_data)
            return result_json
