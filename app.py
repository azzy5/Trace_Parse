from werkzeug.utils import secure_filename
import flask as Flask
from flask import flash
from helpers import Trace_Parser_OP1
from helpers import Trace_Parser_OP3


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
from helpers.utils import  error_class, success_class
from helpers.FormsCheck import TraceInputs
from werkzeug.utils import secure_filename
ALLOWED_EXTENSIONS = {'log', 'out', 'pkt'}

sys.path.append('./helpers')
app = Flask(__name__)
app.secret_key = 'Let it be a secrete'
error_class = 'alert alert-danger'
success_class = 'alert alert-primary'

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

Record Example:
{
"_id": id
"name" : f_name
"f_size": f_size
"comment" : comment_text
"created_at" : created_at
"t_start" : total_starts
"t_exit" : total_exists
"t_duraion" : totol_durations
"s_time" : start_time
"e_time" : end_time
"md5" : file_md5
"data" : [...]
}

Tracker : https://trello.com/b/gVSNGEOf/trace-parser
'''


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route("/show_trace_logs", methods=['GET', 'POST'])
def show_trace_logs():
    try:
        file = open('./helpers/sample_1.json', 'r')
        data = json.load(file)
        file.close()
    except FileNotFoundError:
        print("the file not found, exiting...")
        data = []
    return render_template('traceview.html', data=data)


'''
0. Check if the file exists
1. Save the file
2. Pass the location of file to OP1 and catch the output
3. Pass the output to tarceview
4. log the JSON to DB by creating a record with a qunique ID
5. Delete the uploaded file

'''
@app.route("/snoop_only", methods=['GET', 'POST'])
def show_snoop_logs():
    if request.method == 'GET':
        flash('Looks like you\'re lost, let\'s try again', error_class)
        return render_template("index.html")
    if 'snoop_file' not in request.files or request.files['snoop_file'].name == '':
        flash('Invalid file to be uploaded..', error_class)
        return render_template("index.html")
    else:
        file = request.files['snoop_file']
        if file and allowed_file(file.filename):
            try:
                fname = secure_filename(file.name)
                file.save(fname)
                flash("File Saved", success_class)
                return render_template("index.html")
            except expression:
                flash("Are you sure that's correct file?", error_class)
                return render_template("index.html")
        else:
            flash("Are you sure that's correct file?", error_class)
            return render_template("index.html")

# Trace
@app.route("/trace_only", methods=['GET', 'POST'])
def trace_only():
    if request.method == 'GET':
        flash('Looks like you\'re lost, let\'s try again', error_class)
        return render_template("index.html")

    if 'trace_file' not in request.files or request.files['trace_file'].name == '':
        flash('Invalid file to be uploaded..', error_class)
        return render_template("index.html")
    else:
        file = request.files['trace_file']
        trace_option = request.form['trace_option2']
        print(trace_option)
        if file and allowed_file(file.filename):
            try:
                fname = secure_filename(file.filename)
                file.save(fname)
            except expression:
                flash("Something went wrong", error_class)
                return render_template("index.html")
            if execute(fname, trace_option):  
                try:
                    file = open('./helpers/'+fname+'.json', 'r')
                    data = json.load(file)
                    file.close()
                    return render_template('traceview.html', data=data)
                except FileNotFoundError:
                    print("the file not found, exiting...")
                    data = []
                    flash("Something went wrong while parsing the log...", error_class)
                    return render_template('traceview.html', data=data)
            else:
                flash("Something went wrong while parsing the log...", error_class)
                data = []
                return render_template('traceview.html', data=data)
        else:
            flash("Are you sure that's correct file?", error_class)
            return render_template("index.html")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def execute(fname, trace_option):
    if trace_option=='3':
        return Trace_Parser_OP3.execution(fname)
    if trace_option=='1':
        return Trace_Parser_OP1.execution(fname)
    
if __name__ == '__main__':
    app.run(debug=True)
