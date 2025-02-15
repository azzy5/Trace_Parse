

import json
import datetime
line_f = ""
line_e = ""

'''

2. Lterate through each line and if the line contains "ENTER" then start parsing
3. Start a new JSON object
3. Parse the first line and Append <Date>, <Timestamp>, <PID, PPID>, <Lable>, <Function Name> to local JSON
4. Start parsing the next lines for parameters and create a nested JSON 
5. Keep repeating the step 4 and add the nested JSON to local JSON  until "EXIT" Encountered
6. IF "EXIT" Encountered parse the 

'''

#1. Read file and process the data
def read_file(_fname):
    try:
        file = open(_fname , "r")
        lines_temp = file.readlines()
        file.close()
    except FileNotFoundError:
        pass
    index = 0
    lines = []
    while ( index < len(lines_temp)):
        line = lines_temp[index]
        if(line != '\n'):
            lines.append(line)
        index = index + 1
    return lines



#2. Print statistics
def print_statistics(lines):
    return_json = {}
    Enter_count = 0
    Exit_count =0
    for line in lines:
        if "ENTER" in line:
            Enter_count= Enter_count + 1
    for x,line in enumerate(lines):
        if "EXIT" in line:
            Exit_count= Exit_count + 1
            if  "SQLGetInfo" in line or "SQLGetInfoW" in line:
                d_line = process_line(lines[x+2])[1]
                d_value = lines[x+3].split(']')[-1]
                if len(d_value.split(' ')) > 7:
                    pass
                else:
                    t_data = lines[x+3].split(']')[-1]
                    #print("test :{0},".format(t_data))
                    if d_line == '17' and t_data != "":
                        return_json["db_name"] = t_data
                    if d_line == '18'and t_data != "":
                        return_json["db_ver"] = t_data
                    if d_line == '6' and t_data != "":
                        return_json["diver_file"] = t_data
                    if d_line == '7' and t_data != "":
                        return_json["diver_ver"] = t_data
    line_f = lines[0]
    index = len(lines) - 1
    while index >= 0:
        line = lines[index]
        index = index - 1
        if "EXIT" in line:
            line_e = line
            break
    return_json["start_time"] = line_f.split()[0] + " "+line_f.split()[1]
    #print ("Start time : "+ return_json["start_time"])
    return_json["end_time"] = line_e.split()[0] + " "+line_e.split()[1]
    #print ("End time : " + return_json["end_time"])
    return_json["total_duration"] = time_diff(line_e.split()[0] + " "+line_e.split()[1], line_f.split()[0] + " "+line_f.split()[1])
    #print ("Total time : " + return_json["total_duration"])
    return_json["line_count"] = len(lines)
    #print ("Total number of lines:" +str(return_json["line_count"]))
    return_json["enter_count"] = Enter_count
    #print ("Total number of ENTER:" +str(return_json["enter_count"]))
    return_json["exit_count"] = Exit_count
    #print ("Total number of EXIT:" +str(return_json["exit_count"]))
    return_json["uploaded_at"] = datetime.datetime.now()
    return return_json



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
            local_json = {}
            line = process_line(line)
            local_json["index"] = value_at
            local_json["start_time"] = get_timestamp(line)
            local_json["function_s"] = line[4]
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
            except IndexError:
                pass
            try:
                while "ENTER" not in lines[index] and index < len(lines):
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
                local_json["post_function_parameters"] = nested_array
                nested_array = []
                line = process_line(line_e)
                local_json["end_time"]  =  get_timestamp(line)
                difference = datetime.datetime.strptime(local_json["end_time"], '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(local_json["start_time"], '%Y-%m-%d %H:%M:%S.%f')
                local_json["duration"] = str(difference)
                local_json["function_cc"] =  function_hilighter(difference)
                local_json["function_e"] = line[4]
                local_json["return_code"] = line[-2]
                local_json["result"] = line[-1]
                value_at = value_at + 1
                index = index - 1
                global_json.append(local_json)
            except IndexError:
                pass
        index = index + 1
    return json.dumps(global_json)

def function_hilighter(difference):
    if difference > datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=10, hours=0, weeks=0):
        return "bg-danger"
    if difference > datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=1, hours=0, weeks=0):
        return "bg-warning"
    if difference > datetime.timedelta(days=0, seconds=1, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
        return "bg-info"

'''
1 = Trace Option One
2 = Trace Option Two
3 = Trace Option Tree
4 = Unknown format
'''
def validate(lines):
    index = 0
    while index < len(lines):
        line = lines[index]
        if "ENTER" in line:
            #print(lines[index+1])
            if "pid" in lines[index+1]:
                return 3
            elif "@ws" in lines[index+1]:
                return 2
            else:
                return 1
        index = index + 1
    return 4

            

def execution(file_name):
    global_json = []
    lines = read_file(file_name)
    valdation = validate(lines)
    if valdation == 1:
        statistics = print_statistics(lines)
        data_json = parse_lines(lines)
        file = open('./helpers/temp.json', 'w')
        file.write(data_json)
        file.close()
        return True,statistics
    else:
        return False, "File not formatted for TraceOption=1, try again"

    '''
if __name__ == '__main__':
    lines = read_file('./helpers/TraceOption=2.out')
    validation = validate(lines)
    print("validation : {}".format(validation))


    difference = datetime.datetime.strptime("2019-06-17 07:21:26.000996", '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime("2019-06-17 07:21:11.000676", '%Y-%m-%d %H:%M:%S.%f')
    print(function_hilighter(difference))
    index = 0
    value_at = 0
    while index < len(lines):
        line = process_line(lines[index])
        print(str(index) + str(line))
        index = index + 1
    
    line = process_line(lines[141])
    print(line)
    count = 0
    nested_json = {}
    for value in line:
        nested_json["{}".format(count)] = value
        count = count + 1
    print(nested_json)
    '''

