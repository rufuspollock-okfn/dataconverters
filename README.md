===============
Data Converters
===============

Unified python library to convert data from one format to another. Please file bugs for any unexpected behavior.

[![Build
Status](https://travis-ci.org/okfn/data-converters.png?branch=master)](https://travis-ci.org/okfn/data-converters)

Installation
------------

Clone the repository and run:

    python setup.py install

The CSV and XLS converters use messytables, please manually install messytables with:

    pip install messytables

For Geo functionality we require [Fiona](http://toblerity.github.com/fiona/). This in turn requires the libgdal bindings (see Fiona install instructions for more detail. On Ubuntu I did:

    apt-get install libgdal1-dev
    pip install fiona

Usage
-----

Here's an example parsing CSV to JSON. Note that this isn't just any old csv parsing! Headers (and column names) are extracted, types detected etc etc.

    import dataconverters.csv as csv
    with open('simple.csv') as f:
        # records is an iterator over the records
        # metadata is a dict containing a fields key which is a list of the fields
        records, metadata = csv.csv_parse(f)

API
---

There are 2 types of functionality within Data Converters:

    convert => stream, metadata [, errors]
    parse => results iterator (rows or equivalent), metadata [, errors]

A convert function takes a given input stream of a given format and produces an output stream in a specified output format. For example, converting CSV to JSON (in a specific structure), or taking KML to GeoJSON.

A parse function takes a given input stream and returns python objects in a given structure. For example, CSV is converted to an iterator of rows. Parsing isn't always possible since there may not be a well-defined intermediate, iterable python structure one can hold the data in.

Metadata
========

metadata is a dictionary for holding information extracted during the processing. For example, for tabular data it would include a `fields` key which contained information on the fields (columns) in the table as per the [JSON Table Schema](http://www.dataprotocols.org/en/latest/json-table-schema.html).

Source Types Supported
----------------------

CSV
===

For CSV files, type should be `csv`. Empty column names will be auto-generated with column_1, column_2, etc. Duplicate column names will have _n added as well. For instance, two columns with name date will be date_1, date_2.


XLS(X)
======

For XLS input files type should be `xls`, and for XLSX files, type must be `xlsx`. Empty column names will be auto-generated with column_1, column_2, etc. Duplicate column names will have _n added as well. For instance, two columns with name date will be date_1, date_2.


