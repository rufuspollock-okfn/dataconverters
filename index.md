---
layout: default
---

<h1>
  Data Converters 
  &mdash;
  <a href="http://okfnlabs.org/"><img src="http://assets.okfn.org/p/labs/img/logo-flask.png" alt="" style="height: 40px;" /></a>
</h1>

Unified **python library** and **command line interface** to convert data from
one format to another (especially *tabular* data). Supports:

* CSV (to, from)
* XLS(X) (from)
* JSON (to, from)
* KML to GeoJSON
* Shapefile to GeoJSON

Please [file bugs][issues] for any unexpected behavior.

If you like this sort of thing you may also like [Data Pipes - streaming data transforms in the browser][datapipes]! We have also have a review of [existing libraries and work][existing].

[issues]: https://github.com/okfn/dataconverters/issues
[datapipes]: http://datapipes.okfnlabs.org/
[existing]: docs/existing.html

## Usage

From the command line:

    dataconvert simple.xls out.csv

    # use it with urls
    dataconvert https://github.com/okfn/dataconverters/raw/master/testdata/xls/simple.xls out.csv

    # pipe to stdout
    dataconvert simple.xls _.csv

    # other formats ...
    dataconvert simple.csv _.json

    # if it can't guess the data format ... (simple is an excel file)
    dataoncvert --format=xls simple.i-am-xls-really out.csv

For more details see the help:

    dataconvert -h

### As a Python Library

The basic dataconvert convenience utility makes it very easy to convert data:

    from dataconverters import dataconvert
    dataconvert('infile-or-url.xls', 'outfile.csv')
    dataconvert('infile-or-url.xls', 'outfile.csv', sheet=3)
    dataconvert('infile-or-url.i-am-really-an-xls', 'outfile.csv', format='xls')

Find out more:

    pydoc dataconverters

Here's an example of doing a full parse of CSV to JSON. Note that this isn't
just any old csv parsing! Headers (and column names) are extracted, types
detected etc etc.

    import dataconverters.commas as commas
    with open('simple.csv') as f:
        # records is an iterator over the records
        # metadata is a dict containing a fields key which is a list of the fields
        records, metadata = commas.parse(f)
        print metadata
        print [r for r in records]

For more examples see the source code.


## Installation

Install from PyPI:

    pip install dataconverters

Or you can install from Source:

    # Clone the repository
    https://github.com/okfn/dataconverters
     
    # then install the lib ...
    
    # move into the directory
    cd dataconverters
    
    # install the library
    pip install -e .
    # you can use the more old-fashioned route if you do not have pip
    # python setup.py install

### Additional Dependencies

For Geo functionality we require [Fiona](http://toblerity.github.com/fiona/).
This in turn requires the libgdal bindings (see Fiona install instructions for
more detail. On Ubuntu one does::

    apt-get install libgdal1-dev
    # then install fiona
    pip install fiona


## DataConverters Standard API

There are 2 types of functionality within Data Converters:

* "Parsing": A parse function takes a given input stream and returns python
  objects in a given structure. For example, CSV is converted to an iterator of
  rows. Parsing isn't always possible since there may not be a well-defined
  intermediate, iterable python structure one can hold the data in.
* "Converting": A convert function takes a given input stream of a given format
  and produces an output stream in a specified output format. For example,
  converting CSV to JSON (in a specific structure), or taking KML to GeoJSON.

In code terms method signatures look like:


    def parse(fileobj-like-stream, ....)
        :return: (iterator, metadata)
          where iterator is an iterator over rows / records in the data and
          metadata is metadata about the source (see below)
    
    def convert(fileobj-like-stream, ...)
        :return: (stream, metadata)

There is some variation so some parse function only take a file path rather a file like object.

### Metadata

Metadata is a dictionary for holding information extracted during the
processing. For example, for tabular data it would include a `fields` key which
contained information on the fields (columns) in the table as per the [JSON
Table Schema](http://www.dataprotocols.org/en/latest/json-table-schema.html).


## Source Data Formats Supported

### CSV

For CSV files, type should be `csv`. Empty column names will be auto-generated
with column_1, column_2, etc. Duplicate column names will have _n added as
well. For instance, two columns with name date will be date_1, date_2.


### XLS(X)

For XLS input files type should be `xls`, and for XLSX files, type must be
`xlsx`. Empty column names will be auto-generated with column_1, column_2, etc.
Duplicate column names will have _n added as well. For instance, two columns
with name date will be date_1, date_2.

### KML

We can convert KML to GeoJSON

### Shape

Support for coverting from Shapefiles using Fiona and GDAL.

## License and Credits

Copyright 2007-2013 Open Knowledge Foundation. Licensed under the MIT license.

Developed with generous support from Google.

