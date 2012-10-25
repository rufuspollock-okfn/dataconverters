import json
from StringIO import StringIO
import requests
from unicodecsv import DictReader
from flask import abort, jsonify, request, render_template, Response
from manhunter import app


@app.route('/')
def index():
    return render_template('index.html')


@app.route('api/convert/<format>')
def convert(format=None):
    if (format is None or
            request.args.get('url') is None):
        abort(404)
    r = requests.get(request.args.get('url'))
    csvcontent = StringIO(r.text)
    csvreader = DictReader(csvcontent)
    dictdata = json.dumps([row for row in csvreader])
    return Response(dictdata, mimetype='application/json')

