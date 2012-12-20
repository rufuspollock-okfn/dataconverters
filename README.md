Data Converters
===============

Unified python library to convert data from one format to another.  Please file bugs for any unexpected behavior.

Installation
------------
Clone the repository and run `python setup.py install`. The CXV and XLS converters use messytables, please manually install messytables with `pip install messytables`.

Usage
-----
    from dataconverters import dataconverter

    with open('simple.csv') as f:
        data = dataconverter(f, {'type': 'csv', 'target': 'json'})
        headers, content = data.convert()

Adding the type is optional if the file can be identified from mime-type correctly.

CSV -> JSON
-----------

For CSV files, type should be `csv`. Empty column names will be auto-generated with column_1, column_2, etc. Duplicate column names will have _n added as well. For instance, two columns with name date will be date_1, date_2.

XLS(X) -> JSON
--------------

For XLS input files type should be `xls`, and for XLSX files, type must be `xlsx`. Empty column names will be auto-generated with column_1, column_2, etc. Duplicate column names will have _n added as well. For instance, two columns with name date will be date_1, date_2.
