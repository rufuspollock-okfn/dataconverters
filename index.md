---
layout: default
title: Data Converters 
---

Unified **python library** and **command line interface** to convert data from
one format to another (especially *tabular* data). Supports:

* CSV (to, from) - with type detection (dates, numbers etc)
* XLS(X) (from) - ditto
* JSON (to, from)
* KML to GeoJSON
* Shapefile to GeoJSON

Please [file bugs][issues] for any unexpected behavior. If you like this sort of thing you may also like [Data Pipes - streaming data transforms in the browser][datapipes]!

Copyright 2007-2013 Open Knowledge Foundation. Licensed under the MIT license. Developed with generous support from Google.

[issues]: https://github.com/okfn/dataconverters/issues
[datapipes]: http://datapipes.okfnlabs.org/
[existing]: docs/existing.html

**Table of Contents**

* This will become a table of contents (this text will be scraped).
{:toc}

## Usage

### Command line

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

----

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

----

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

----

## Research - Existing Libraries and Services

Please [add to this list &raquo;][edit]

[edit]: https://github.com/okfn/dataconverters/edit/master/index.md

<table class="table-bordered table" style="font-size: 75%;">
  <tr>
    <th>Source</th>
    <th>Dest</th>
    <th>Services</th>
    <th>Libraries</th>
    <th>Comments</th>
  </tr>
  <tr>
    <td>CSV</td>
    <td>...</td>
    <td>
      https://github.com/okfn/dataproxy
    </td>
    <td>
      Reasonably straightforward to do in most programming languages
    </td>
    <td>
      See https://github.com/okfn/dataconverters/issues/2
    </td>
  </tr>
  <tr>
    <td>XLS</td>
    <td></td>
    <td>
<a href="https://github.com/stephenjudkins/poisauce">Gut implementation</a>, <a href="https://github.com/okfn/dataproxy">DataProxy</a>
    </td>
    <td>
* xlrd (python)
* POI (Java)
* messytables (builds on xlrd)
    </td>
    <td>
See https://github.com/okfn/dataconverters/issues/6
    </td>
  </tr>
  <tr>
    <td>Shapefiles</td>
    <td>...</td>
    <td>
    </td>
    <td>
* GDAL and OGR
* QGIS (tool) - not open
    </td>
    <td>
See https://github.com/okfn/dataconverters/issues/1
    </td>
  </tr>
  <tr>
    <td>KML</td>
    <td>...</td>
    <td>
    </td>
    <td>
* GDAL can do this (but no Fiona bindings) - but see https://github.com/Toblerity/Fiona/issues/23
* fastkml https://github.com/cleder/fastkml
* sgillies keytree
    </td>
    <td>
See https://github.com/okfn/dataconverters/issues/5
    </td>
  </tr>
  <tr>
    <td>GeoJSON</td>
    <td>...</td>
    <td></td>
    <td></td>
    <td>Can parse with normal libraries</td>
  </tr>
  <tr>
    <td>PDF</td>
    <td>...</td>
    <td>
    </td>
    <td>
    </td>
    <td>
- See overview and list here https://gist.github.com/rgrp/5844485
- Also the issue https://github.com/okfn/dataconverters/issues/9
- and <a href="http://schoolofdata.org/handbook/courses/extracting-data-from-pdf/">School of Data intro</a>
    </td>
  </tr>
  <tr>
    <td>Access (MDB)</td>
    <td>...</td>
    <td>
    </td>
    <td>
http://mdbtools.sourceforge.net/
    </td>
    <td>
See https://github.com/okfn/dataconverters/issues/10
    </td>
  </tr>
</table>

