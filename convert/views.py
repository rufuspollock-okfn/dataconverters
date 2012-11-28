import json
from StringIO import StringIO
from tempfile import NamedTemporaryFile, TemporaryFile
import requests
from flask import request, render_template, Response
from convert import app
from convert.dataconverter import dataconverter
from convert.util import crossdomain, jsonpify


cors_headers = ['Content-Type', 'Authorization']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/convert/<format>')
@crossdomain(origin='*', headers=cors_headers)
@jsonpify
def convert(format=None):
    results = {}
    if (format is None or
            request.args.get('url') is None):
        results['error'] = error
        results = json.dumps(results)
    else:
        url = request.args.get('url')
        r = requests.get(url)
        handle = StringIO(r.content)
        with NamedTemporaryFile() as datafile:
            datafile.write(handle.getvalue())
            datafile.seek(0)
            data = dataconverter(datafile, request.args)
            try:
                data = dataconverter(datafile, request.args)
                header, results = data.convert()
                results_json = json.dumps({'headers': header, 'data': results})
            except Exception as e:
                results['error'] = str(e)
                results_json = json.dumps(results)
    return Response(results_json, mimetype='application/json')
