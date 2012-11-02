import json
from flask import request, render_template, Response
from manhunter import app
from manhunter.transform import transformer
from manhunter.util import crossdomain, jsonpify


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
            data = transformer(url, request.args)
            results = data.transform()
        except Exception as e:
            results['error'] = str(e)
            results = json.dumps(results)
    return Response(results, mimetype='application/json')
