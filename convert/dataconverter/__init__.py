from base import *


import csv_json_converter
import xls_json_converter


register_dataconverter({
        "name": "csv",
        "class": csv_json_converter.CSVConverter,
        "mime_types": ["text/csv", "text/comma-separated-values"],
})


register_dataconverter({
        "name": "xls",
        "class": xls_json_converter.XLSConverter,
        "mime_types": ["application/vnd.ms-excel", "application/excel"],
})


register_dataconverter({
        "name": "xlsx",
        "class": xls_json_converter.XLSXConverter,
        "mime_types": ['application/vnd.openxmlformats-officedocument.'
                      'spreadsheetml.sheet'],
})
