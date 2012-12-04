from base import *


import csv_json_converter
import xls_json_converter


register_dataconverter({
        "name": "csv",
        "class": csv_json_converter.CSVConverter,
        "extensions": ['csv'],
        "mime_types": ["text/csv", "text/comma-separated-values"],
})


register_dataconverter({
        "name": "xls",
        "class": xls_json_converter.XLSConverter,
        "extensions": ['xls'],
        "mime_types": ["application/excel"],
})


register_dataconverter({
        "name": "xlsx",
        "class": xls_json_converter.XLSXConverter,
        "extensions": ['xlsx'],
        "mime_types": ["application/vnd.ms-excel",
                      'application/vnd.openxmlformats-officedocument.'
                      'spreadsheetml.sheet'],
})
