__all__ = ['dataconvert']

import dataconverters.commas as dcsv
import urllib2
import mimetypes
import sys
import itertools

def dataconvert(inpath, outpath,
        sheet=1,
        guess_types=False,
        records=None,
        format='', 
        encoding=''
        ):
    '''Run a data conversion based on args object.

    @param inpath: path / url to file
    @parma outpath: path to resulting output

    all other arguments are like the arguments to dataconvert command line tool
    (e.g. --records on command line becomes records=... kw argument)

    Example:

        from dataconverters import dataconvert
        dataconvert('myfile.xls', 'myfile.csv')
    '''
    args = AttrDict(locals())
    _dataconvert(args)

# HACK: args can come either from CLI in which case not dict and has
# attribute OR can come from normal client user in which case we need
# attribute style access
def _dataconvert(args):
    if args.format:
        intype = args.format
    else:
        intype = guess_type(args.inpath)
    outtype = guess_type(args.outpath)

    if is_url_path(args.inpath):
        instream = urllib2.urlopen(args.inpath)
    else:
        instream = open(args.inpath)

    # tsv_types = ['tsv', 'text/tsv', 'text/tab-separated-values']
    if intype in ['text/csv', 'csv']:
        records, metadata = dcsv.parse(instream, guess_types=args.guess_types)
    elif intype in ['application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'xls'
        ]:
        import dataconverters.xls
        excel_type = 'xls' if intype == 'application/vnd.ms-excel' else 'xlsx'
        records, metadata = dataconverters.xls.parse(instream,
                excel_type=excel_type,
                sheet=args.sheet,
                guess_types=args.guess_types,
                encoding=args.encoding
                )
    else:
        raise ValueError(
            'No support for reading file type %s - support for csv or xls only at present' % intype)

    if args.outpath.startswith('_.'):
        outstream = sys.stdout
    else:
        outstream = open(args.outpath, 'w')

    if (args.records):
        records = itertools.islice(records, int(args.records))

    if outtype == 'text/csv':
        dcsv.write(outstream, records, metadata)
    elif outtype == 'application/json':
        import dataconverters.jsondata as js
        js.write(outstream, records, metadata)
    else:
        raise ValueError('Only support writing to csv and json at present')

def guess_type(path):
    out = mimetypes.guess_type(path)
    return out[0]

def is_url_path(path):
    schemes = ['http', 'https', 'ftp'] 
    for s in schemes:
        if path.startswith(s + '://'):
            return True
    return False

class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

