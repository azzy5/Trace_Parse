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


@app.route("/show_trace_logs", methods=['GET', 'POST'])
def show_trace_logs():
    try:
        file = open('./helpers/sample_1.json','r')
        data = json.load(file)
        file.close()
    except FileNotFoundError:
        print("the file not found, exiting...")
        data= []
    return render_template('traceview.html', data=data)

@app.route("/show_snoop_logs", methods=['GET', 'POST'])
def show_snoop_logs():
    if request.method == 'POST':
        f = request.files['snoop_file']
        fname = f.filename
        dirname = os.getcwd()
        print(dirname)
        if fname == '':
            flash("Are you sure that's correct file?",error_class)
            return render_template("index.html")
        else:
            try:
                f.save(secure_filename(f.filename))
            except expression as identifier:
                flash("Are you sure that's correct file?",error_class)
                return render_template("index.html")
            finally:
                flash("File Saved",success_class)
                return render_template("index.html")
    else:
        flash("Somethin Wrong, try again",error_class)
        return render_template("index.html")


@app.route("/trace_only", methods=['GET', 'POST'])
def trace_only():
    if request.method == 'POST':
        f = request.files['trace_file']
        fname = f.filename
        dirname = os.getcwd()
        print(dirname)
        if fname == '':
            flash("Are you sure that's correct file?",error_class)
            return render_template("index.html")
        else:
            try:
                f.save(secure_filename(f.filename))
            except expression as identifier:
                flash("Are you sure that's correct file?",error_class)
                return render_template("index.html")
            finally:
                flash("File Saved",success_class)
                return render_template("index.html")
    else:
        flash("Somethin Wrong, try again",error_class)
        return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
