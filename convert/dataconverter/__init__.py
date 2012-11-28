from base import *


import csv_json_converter
import xls_json_converter


register_dataconverter({
        "name": "csv",
        "class": csv_json_converter.CSVConverter,
})


register_dataconverter({
        "name": "xls",
        "class": xls_json_converter.XLSConverter,
})
