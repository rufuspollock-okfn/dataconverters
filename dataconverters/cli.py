import argparse
from dataconverters import _dataconvert

def make_argparser():
    parser = argparse.ArgumentParser(description=\
'''Convert data between formats. Supported formats:

    Input:  csv, tsv, excel (xls, xlsx).
    Output: csv, json

Examples
========

# convert from simple.xls file online to out.csv in current directory
dataconvert https://github.com/okfn/dataconverters/raw/master/testdata/xls/simple.xls out.csv

# convert from simple.xls to json on stdout
dataconvert https://github.com/okfn/dataconverters/raw/master/testdata/xls/simple.xls _.json

Help
====
''',
    epilog=\
'''Copyright Open Knowledge Foundation 2007-2013. Licensed under the MIT license.
Part of the DataConverters project: https://github.com/okfn/dataconverters''',
     formatter_class=argparse.RawDescriptionHelpFormatter
)
    parser.add_argument('inpath', metavar='inpath', type=str,
                       help='in file path or url')
    parser.add_argument('outpath', metavar='outpath', type=str,
                       help='out file path to write to (use underscore "_" as filename to indicate stdout e.g. _.csv or _.json)')
    parser.add_argument('--no-guess-types', dest='guess_types',
        action='store_false',
        help='''Disable type-guessing (where it is used e.g. with CSVs). Type guessing may significantly affect performance''',
        default=True
        )
    parser.add_argument('--sheet', metavar='NUM',
        help='''Index of sheet in spreadsheet to convert (index starts at 1)''',
        default=1
        )
    parser.add_argument('--records', metavar='NUM',
        help='''Only convert a maximum of NUM records'''
        )
    parser.add_argument('--format',
        help='''Format or mimetype of incoming file e.g. xls, csv, text/csv'''
        )
    parser.add_argument('-e', '--encoding',
        help='''File encoding of incoming file'''
        )
    return parser

def main():
    parser = make_argparser()
    args = parser.parse_args()
    _dataconvert(args)

