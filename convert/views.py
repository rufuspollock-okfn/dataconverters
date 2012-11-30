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


@app.route('/api/convert/<format>', methods=['GET', 'POST'])
@crossdomain(origin='*', headers=cors_headers)
@jsonpify
def convert(format=None):
    results = {}
    if request.method == 'GET':
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
        handle = StringIO(r.content)
        with NamedTemporaryFile() as datafile:
            datafile.write(handle.getvalue())
            datafile.seek(0)
            try:
                data = dataconverter(datafile, request.args)
                header, results = data.convert()
                results_json = json.dumps({'headers': header, 'data': results})
            except Exception as e:
                results['error'] = str(e)
                results_json = json.dumps(results)
        return Response(results_json, mimetype='application/json')
    uploaded_file = request.files['file']
    if uploaded_file:
        filename = secure_filename(uploaded_file.filename)
        uploaded_file_path = os.path.join(app.config['TMP_FOLDER'], filename)
        uploaded_file.save(uploaded_file_path)
        with open(uploaded_file_path, 'r') as f:
            try:
                data = dataconverter(f, request.form)
                header, results = data.convert()
                results_json = json.dumps({'headers': header, 'data': results})
            except Exception as e:
                results['error'] = str(e)
                results_json = json.dumps(results)
        os.remove(uploaded_file_path)
        return Response(results_json, mimetype='application/json')

