from base import *

import csv_json_transform

register_transformer({
        "name": "csv",
        "class": csv_json_transform.CSVTransformer,
        "mime_types": ["text/csv", "text/comma-separated-values"]})
