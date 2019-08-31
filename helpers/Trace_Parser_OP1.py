

import json
import datetime
line_f = ""
line_e = ""



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
    while ( index < len(lines_temp)):
        line = lines_temp[index]
        if(line != '\n'):
            lines.append(line)
        index = index + 1
    if 2 > len(lines):
        print("File too small to process")
        exit(0)
    print("Processing completed")
    return lines



#2. Print statistics
def print_statistics(lines):
    Enter_count = 0
    Exit_count =0
    for line in lines:
        if "ENTER" in line:
            Enter_count= Enter_count + 1
    for line in lines:
        if "EXIT" in line:
            Exit_count= Exit_count + 1
    line_f = lines[0]
    index = len(lines) - 1
    while index >= 0:
        line = lines[index]
        index = index - 1
        if "EXIT" in line:
            line_e = line
            break
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
    for x in range(len(line)):
        line[x] = line[x].replace("\n", "")
        line[x] = line[x].replace("\t", "")
        line[x] = line[x].replace("\\x00", "")
        line[x] = line[x].replace("\"", "")
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
    global_json = []
    index = 0
    value_at = 0
    while index < len(lines):
        line = lines[index]
        if "ENTER" in line:
            print(line)
            local_json = {}
            line = process_line(line)
            local_json["index"] = value_at
            local_json["start_time"] = get_timestamp(line)
            local_json["function"] = line[4]
            local_json["ppid"] = line[2]
            local_json["info"] = ' '.join(line[5:])
            index = index + 1
            nested_array = []
            try:
                while "EXIT" not in lines[index] and index < len(lines):
                    line = lines[index]
                    line = process_line(line)
                    nested_json = {}
                    count = 0
                    for value in line:
                        nested_json["{}".format(count)] = value
                        count = count + 1
                    nested_array.append(nested_json)
                    nested_json = {}
                    index = index + 1
                local_json["pre_function_parameters"] = nested_array
                nested_array = []
                line_e = lines[index]
                index = index + 1
                print(lines[index])
            except IndexError:
                print(index)
            try:
                while "ENTER" not in lines[index] and index < len(lines):
                    line = lines[index]
                    line = process_line(line)
                    nested_json = {}
                    for value in line:
                        nested_json["{}".format(count)] = value
                        count = count + 1
                    nested_array.append(nested_json)
                    nested_json = {}
                    index = index + 1
                local_json["post_function_parameters"] = nested_array
                nested_array = []
                line = process_line(line_e)
                local_json["end_time"]  =  get_timestamp(line)
                difference = datetime.datetime.strptime(local_json["end_time"], '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(local_json["start_time"], '%Y-%m-%d %H:%M:%S.%f')
                local_json["duration"] = str(difference.microseconds)
                local_json["return_code"] = line[-2]
                local_json["result"] = line[-1]
                value_at = value_at + 1
                index = index - 1
                global_json.append(local_json)
            except IndexError:
                print(index)
        index = index + 1
    return json.dumps(global_json)

def validate(lines):
    index = 0
    while index < len(lines):
        line = lines[index]
        if "ENTER" in line:
            line = process_line(line)
            

def execution():
    global_json = {}
    lines = read_file("./helpers/TraceOption=1.out")
    print_statistics(lines)
    json = parse_lines(lines)
    print("opening the file ....")
    file = open('./helpers/sample_1.json', 'w')
    print("Writing data to file  ....")
    file.write(json)
    file.close()
    print("Completed  ....")
    return True


if __name__ == '__main__':
    execution()

''' To print all lines
    index = 0
    value_at = 0
    while index < len(lines):
        line = process_line(lines[index])
        print(str(index) + str(line))
        index = index + 1
'''

'''
    line = process_line(lines[141])
    print(line)
    count = 0
    nested_json = {}
    for value in line:
        nested_json["{}".format(count)] = value
        count = count + 1
    print(nested_json)
'''
