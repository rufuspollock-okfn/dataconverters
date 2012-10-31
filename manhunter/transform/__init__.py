from base import *

import csv_transform

register_transformer({
        "name": "csv",
        "class": csv_transform.CSVTransformer,
        "extensions": ["csv", "tsv"],
        "mime_types": ["text/csv", "text/comma-separated-values"]})
