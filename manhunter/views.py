from flask import jsonify, request, render_template
from manhunter import app
from manhunter.transform import transformer


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/convert/<format>')
def convert(format=None):
    results = {}
    error = None
    if (format is None or
            request.args.get('url') is None):
        error = 'No URL set'
    else:
        url = request.args.get('url')
        data = transformer('csv', url, {})
        results['data'] = data.transform()
    results['error'] = error
    return jsonify(results)
