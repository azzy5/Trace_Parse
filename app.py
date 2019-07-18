import flask as Flask

try:
    import sys
except ImportError:
    print('sys : Module not found.  ')
try:
    import os
except ImportError:
    print('os : Module not found')
try:
    from flask import *
except ImportError:
    print('flask : Module not found')

try:
    import json
except ImportError:
    print('  json : library not found.  ')
    print('flask : Module not found')

try:
    import requests
except ImportError:
    print('  requests : library not found.  ')

try:
    import urllib
except ImportError:
    print(' urllib : library not found.  ')

sys.path.append('./helpers')
from helpers.Trace_Parser_7 import *

data = []
app = Flask(__name__)
app.secret_key = 'Let it be a secrete'


@app.route("/", methods=['GET', 'POST'])
def index():
    #with open('sample.json') as json_file:
    #    data = json.load(json_file)
    #result =  execution()
    result = True
    if result:
        file  = open('./helpers/sample.json','r')
        data = json.load(file)
        file.close()
    else:
        data = None
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=False)
