#!/usr/bin/python

import json
import datetime



#1. Read file and process the data
def read_file(_fname):
    try:
        print("Opening file :" + _fname)
        file = open(_fname , "r")
        lines_temp = file.readlines()
        file.close()
        print("File reading completed ...")
    except FileNotFoundError:
        print("the file not found, exiting...")
        exit(0)
    index = 0
    lines = []
    print("Processing file ...")
    #if(len(lines) < 2):
     #   print("File too small to process")
     #   exit(0)
    while ( index < len(lines_temp)):
        line = lines_temp[index]
        if(line != '\n'):
            lines.append(line)
        index = index + 1
    print("Processing completed")
    return lines

#2. Print statistics
def print_statistics(lines):
    Enter_count = 0
    Exit_count =0
    for line in lines:
        if "ENTER" in line:
            Enter_count= Enter_count +1
    for line in lines:
        if "EXIT" in line:
            Exit_count= Exit_count +1
    line_f = lines[0]
    line_e = lines[-1]
    print ("Start time : " + line_f.split()[0] + " "+line_f.split()[1])
    print ("End time : " + line_e.split()[0] + " "+line_e.split()[1])
    print ("Total time : " + time_diff(line_e.split()[0] + " "+line_e.split()[1], line_f.split()[0] + " "+line_f.split()[1]))
    print ("Total number of lines:" +str(len(lines)))
    print ("Total number of ENTER:" +str(Enter_count))
    print ("Total number of EXIT:" +str(Exit_count))

def process_line(line):
    line = line.split(' ')
    while "" in line:
        line.remove("")
    return line

def time_diff(line1, line2):
    return str(datetime.datetime.strptime(line1.split()[0] + " "+line1.split()[1], '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(line2.split()[0] + " "+line2.split()[1], '%Y-%m-%d %H:%M:%S.%f'))

def time_diff_with_string(time_s, time_e):
    return str(datetime.datetime.strptime(time_e, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(time_s, '%Y-%m-%d %H:%M:%S.%f'))


def get_timestamp(line):
    return str(datetime.datetime.strptime(line[0] + " " + line[1], '%Y-%m-%d %H:%M:%S.%f'))


def get_timestamp_with_string(line):
    return str(datetime.datetime.strptime(line[0] + " " + line[1], '%Y-%m-%d %H:%M:%S.%f'))

def parse_lines(lines):
    lines = lines
    global_json = []
    index = 0
    value_at = 0
    while index < len(lines):
        line =  lines[index]
        if "ENTER" in line:
            local_json = {}
            line = process_line(line)
            local_json["index"] = value_at
            local_json["start_time"] = get_timestamp(line)
            local_json["function"] = line[4]
            local_json["ppid"] = line[2]
            local_json["info"] = ' '.join(line[5:])
            index = index + 1
            nested_array = []
            while "EXIT" not in lines[index]:
                nested_json = {}
                line = lines[index]
                line = process_line(line)
                nested_json["timestamp"] =  get_timestamp(line)
                nested_json["ppid"] = line[2]
                nested_json["type"] = line[3]
                nested_json["value"] = line[4]
                if len(line) == 6:
                    nested_json["sql_const"] = line[5]
                else:
                    nested_json["type"] = ''
                nested_array.append(nested_json)
                index = index + 1
            local_json["function_parameters"] = nested_array
            line = lines[index]
            line = process_line(line)
            local_json["end_time"]  =  get_timestamp(line)
            difference = datetime.datetime.strptime(local_json["end_time"], '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(local_json["start_time"], '%Y-%m-%d %H:%M:%S.%f')
            local_json["duration"] = str(difference.microseconds)
            local_json["return_code"] = line[-2]
            local_json["result"] = line[-1]
            value_at = value_at + 1
            global_json.append(local_json)
        index = index + 1
    return global_json




'''
['2019-07-11', '04:23:01.992958', 'ppid=13631576:pid=14024888:1:', '\tENTER', 'SQLGetInfo', 'called', 'by', 'Progress', 'DataDirect', 'trace', 'library\n']
['2019-07-11', '04:23:01.996347', 'ppid=13631576:pid=14024888:1:', '\tENTER', 'SQLGetInfo', '\n']

['2019-07-11', '05:27:39.982952', '(Time', 'elapsed', 'in', 'microseconds', ':', '34)', 'ppid=13631576:pid=14024888:1:', '\tEXIT', 'SQLRowCount', 'with', 'return', 'code', '0', '(SQL_SUCCESS)\n']
16
['2019-07-11', '04:23:01.992506', '(Time', 'elapsed', 'in', 'microseconds', ':', '62)', 'ppid=13631576:pid=14024888:1:', '\tEXIT', 'SQLGetInfo', 'called', 'by', 'Progress', 'DataDirect', 'trace', 'library', 'with', 'return', 'code', '0', '(SQL_SUCCESS)\n']
22

['2019-07-11', '04:22:59.432795', 'ppid=13631576:pid=14024888:1:', '\tHENV', '00000001102cfe10\n']
5
['2019-07-11', '04:23:00.622628', 'ppid=13631576:pid=14024888:1:', '\tSQLSMALLINT', '1', '<SQL_HANDLE_ENV>\n']
6


2. Lterate through each line and if the line contains "ENTER" then start parsing
3. Start a new JSON object
3. Parse the first line and Append <Date>, <Timestamp>, <PID, PPID>, <Lable>, <Function Name> to local JSON
4. Start parsing the next lines for parameters and create a nested JSON 
5. Keep repeating the step 4 and add the nested JSON to local JSON  until "EXIT" Encountered
6. IF "EXIT" Encountered parse the 

'''

if __name__ == '__main__':
    global_json = {}
    lines = read_file("test.txt")
    #print_statistics(lines)
    print(json.dumps(parse_lines(lines)))
