import flask as Flask
from flask import flash


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
from utils import *
from helpers.FormsCheck import TraceInputs
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'Let it be a secrete'



'''
API Routes :

1. POST \trace_only\{file.log, traceoption}
    - Readfile locally and move it to 
    - Validate the 'TraceOption'
    - Parse log to JSON based on the Trace option value
    - Process JSON ????? (maeybe exctract useful info?)
    - Log the log into MongoDB
    <-- Json equelent of log file
    

1. POST \snoop_only\{file.log, traceoption}
    - Readfile locally and move it to 
    - Validate the 'TraceOption'
    - Parse log to JSON based on the Trace option value
    - Process JSON ????? (maeybe exctract useful info?)
    - Log the log into MongoDB
    <-- Json equelent of log file

Tracker : https://trello.com/b/gVSNGEOf/trace-parser
'''

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST' and 'trace_file' in request.files:
        f = request.files['trace_file']
        fname = os.path.splitext(f.filename)
        dirname = os.getcwd()
        print(dirname)
        f.save(secure_filename(f.filename))
        return render_template("index.html", )


    '''  
    result = execution()
    if result:
        try:
            file = open('sample.json','r')
            data = json.load(file)
            file.close()
        except FileNotFoundError:
            print("the file not found, exiting...")
            data= []
    '''


if __name__ == '__main__':
    app.run(debug=True)
