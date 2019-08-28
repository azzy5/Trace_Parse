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
from helpers.FormsCheck import TraceInputs
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'Let it be a secrete'



'''
Routes :

1. POST TraceOption=1 Json
    --> \traceoptin1\{file.log, traceoption}
    - Validate the TraceOption=1
    - Parse log to JSON
    - Process JSON ?????
    - Log the log into MongoDB
    <-- Json equelent of log file
    
2. POST TraceOption=2 Json
    --> \traceoptin1\{file.log, traceoption}
    - Validate the TraceOption=2
    - Parse log to JSON
    - Process JSON ?????
    - Log the log into MongoDB
    <-- Json equelent of log file
    
3. POST TraceOption=3 Json
       --> \traceoptin1\{file.log, traceoption}
    - Validate the TraceOption=3
    - Parse log to JSON
    - Process JSON ?????
    - Log the log into MongoDB
    <-- Json equelent of log file
    
4. 
https://www.programcreek.com/python/example/51528/flask.request.files
'''

@app.route("/", methods=['GET', 'POST'])
def index():
    form = TraceInputs()
    return render_template('index.html',form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST' and 'trace_file' in request.files:
        f = request.files['trace_file']
        fname = os.path.splitext(f.filename)
        dirname = os.getcwd()

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
