import json
import os
from StringIO import StringIO
from tempfile import NamedTemporaryFile, TemporaryFile
import requests
from werkzeug import secure_filename
from flask import request, render_template, Response
from convert import app
from convert.dataconverter import dataconverter
from convert.util import crossdomain, jsonpify


cors_headers = ['Content-Type', 'Authorization']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/convert/<format>', methods=['GET'])
@crossdomain(origin='*', headers=cors_headers)
@jsonpify
def convert_get(format=None):
    results = {}
    metadata = request.args.to_dict()
    if (format is None or
            request.args.get('url') is None):
        results['error'] = 'No format or URL specified'
        results_json = json.dumps(results)
        return Response(results_json, mimetype='application/json')
    url = request.args.get('url')
    r = requests.get(url)
    if requests.codes.ok != r.status_code:
        results['error'] = error
        results_json = json.dumps(results)
        return Response(results_json, mimetype='application/json')
    metadata['mime_type'] = r.headers['content-type']
    handle = StringIO(r.content)
    with NamedTemporaryFile() as datafile:
        datafile.write(handle.getvalue())
        datafile.seek(0)
        try:
            data = dataconverter(datafile, metadata)
            header, results = data.convert()
            results_json = json.dumps({'headers': header, 'data': results})
        except Exception as e:
            results = {}
            results['error'] = str(e)
            results_json = json.dumps(results)
    return Response(results_json, mimetype='application/json')


@app.route('/api/convert/<format>', methods=['POST'])
@crossdomain(origin='*', headers=cors_headers)
@jsonpify
def convert_post(format=None):
    uploaded_file = request.files['file']
    metadata = request.form.to_dict()
    if not uploaded_file:
        results['error'] = 'No file uploaded'
        results_json = json.dumps(results)
        return Response(results_json, mimetype='application/json')
    metadata['mime_type'] = uploaded_file.content_type
    try:
        data = dataconverter(uploaded_file.stream, metadata)
        header, results = data.convert()
        results_json = json.dumps({'headers': header, 'data': results})
    except Exception as e:
        results['error'] = str(e)
        results_json = json.dumps(results)
    return Response(results_json, mimetype='application/json')

