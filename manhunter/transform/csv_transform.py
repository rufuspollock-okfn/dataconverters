"""Data Proxy - CSV transformation adapter"""
from messytables import (
    CSVTableSet,
    headers_guess,
    headers_processor,
    offset_processor)
import requests
import base
from StringIO import StringIO


class CSVTransformer(base.Transformer):

    def __init__(self, url, query):
        super(CSVTransformer, self).__init__(url, query)

        if 'encoding' in self.query:
            self.encoding = self.query["encoding"].value
        else:
            self.encoding = 'utf-8'

        if 'dialect' in self.query:
            self.dialect = self.query["dialect"].value
        else:
            self.dialect = None

    def transform(self):
        csvdata = requests.get(self.url)
        handle = StringIO(csvdata.text.encode('utf-8'))

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
        return result
