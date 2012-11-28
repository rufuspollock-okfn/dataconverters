from base import *


import csv_json_dataconverter
import xls_json_dataconverter


register_dataconverterer({
        "name": "csv",
        "class": csv_json_dataconverter.CSVConverter,
        "mime_types": ["text/csv", "text/comma-separated-values"]})

register_dataconverterer({
        "name": "xls",
        "class": xls_json_dataconverter.XLSConverter,
        "mime_types": ["application/excel", "application/vnd.ms-excel",
                       'application/vnd.openxmlformats-officedocument.'
                       'spreadsheetml.sheet']})
