"""Data Proxy - CSV transformation adapter"""
import json
from StringIO import StringIO
from messytables import (
    CSVTableSet,
    headers_guess,
    headers_processor,
    offset_processor)
import requests
import base


class CSVTransformer(base.Transformer):

    def transform(self):
        csvdata = requests.get(self.url)
        handle = StringIO(csvdata.content)

        table_set = CSVTableSet.from_fileobj(handle)
        row_set = table_set.tables.pop()
        offset, headers = headers_guess(row_set.sample)
        row_set.register_processor(headers_processor(headers))
        row_set.register_processor(offset_processor(offset + 1))

        info = {}
        result = []
        for row in row_set:
            for index, cell in enumerate(row):
                info[cell.column] = cell.value
            result.append(info)
        result_data = {'headers': headers, 'data': result}
        result_json = json.dumps(result_data)
        return result_json
