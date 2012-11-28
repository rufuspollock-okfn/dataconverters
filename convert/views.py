import json
from flask import request, render_template, Response
from convert import app
from convert.dataconverter import transformer
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
        try:
            data = dataconverterer(url, request.args)
            results = data.dataconverter()
        except Exception as e:
            results['error'] = str(e)
            results = json.dumps(results)
    return Response(results, mimetype='application/json')
