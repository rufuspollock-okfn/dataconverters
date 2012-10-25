import json
from StringIO import StringIO
import requests
from unicodecsv import DictReader
from flask import abort, jsonify, request, render_template, Response
from manhunter import app


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/convert/<format>')
def convert(format=None):
    if (format is None or
            request.args.get('file') is None or
            request.args.get('from') is None):
        abort(404)
    r = requests.get(request.args.get('file'))
    csvcontent = StringIO(r.text)
    csvreader = DictReader(csvcontent)
    dictdata = json.dumps([row for row in csvreader])
    return Response(dictdata, mimetype='application/json')

