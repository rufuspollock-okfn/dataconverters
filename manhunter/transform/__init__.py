from base import *


import csv_json_transform
import xls_json_transform


register_transformer({
        "name": "csv",
        "class": csv_json_transform.CSVTransformer,
        "mime_types": ["text/csv", "text/comma-separated-values"]})

register_transformer({
        "name": "xls",
        "class": xls_json_transform.XLSTransformer,
        "mime_types": ["application/excel", "application/vnd.ms-excel",
                       'application/vnd.openxmlformats-officedocument.'
                       'spreadsheetml.sheet']})
