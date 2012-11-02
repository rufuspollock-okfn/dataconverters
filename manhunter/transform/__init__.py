from base import *

import csv_transform

register_transformer({
        "name": "csv",
        "class": csv_transform.CSVTransformer,
        "mime_types": ["text/csv", "text/comma-separated-values"]})
