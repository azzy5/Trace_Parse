
import json
import datetime


def process_line(line):
    if '  ' in line:
        line = line.split('  ')
    else:
        line = line.split('\t')
    while "" in line:
        line.remove("")
    for x in range(len(line)):
        line[x] = line[x].replace("\n", "")
        line[x] = line[x].replace("\t", "")
        line[x] = line[x].replace("\\x00", "")
        line[x] = line[x].replace("\"", "")
    return line

def process_line_2(line):
    line = line.split(' ')
    while "" in line:
        line.remove("")
    for x in range(len(line)):
        line[x] = line[x].replace("\n", "")
        line[x] = line[x].replace("\t", "")
        line[x] = line[x].replace("\\x00", "")
        line[x] = line[x].replace("\"", "")
    return line

def read_file(_fname):
    try:
        print("Opening file :" + _fname)
        file = open(_fname , "r")
        lines_temp = file.readlines()
        file.close()
        print("File reading completed ...")
    except FileNotFoundError:
        print("the file not found, exiting...")
    index = 0
    lines = []
    while ( index < len(lines_temp) ):
        line = lines_temp[index]
        if(line != '\n'):
            lines.append(line)
        index = index + 1
    return lines


def get_timestamp(line):
    return str(datetime.datetime.strptime(line[0] + " " + line[1], '%Y-%m-%d %H:%M:%S.%f'))

def parse_lines(lines):
    global_json =[]
    index = 0
    value_at = 0
    while index < len(lines):
        line = lines[index]
        if "Read:" in line:
            local_json = {}
            current_line = process_line_2(line)
            previous_line = process_line_2(lines[index-1])
            local_json["index"] =  value_at 
            local_json["packet_type"] = current_line[1]
            local_json["packet_size"] = current_line[2]
            local_json["packet_id"] = current_line[0]
            local_json["time_stamp"] = get_timestamp(previous_line)
            nested_data=[]
            index = index + 1

            try:
                while "Read:" not in lines[index] and "Send:" not in lines[index] and index < len(lines):
                    line = process_line(lines[index])
                    if len(line) > 1:
                        nested_data.append(line[1])
                    #nested_data.append(line[1] if len(line) > 0 else None)
                    #continue_ = True if "Read:" not in lines[index] and "Send:" not in lines[index] else False
                    #if continue_:
                    index = index + 1
                local_json["data"] = nested_data
                value_at = value_at + 1
                index = index - 1
            except:
                pass
            global_json.append(local_json)
        if "Send:" in line:
            local_json = {}
            current_line = process_line_2(line)
            previous_line = process_line_2(lines[index-1])
            local_json["index"] =  value_at 
            local_json["packet_type"] = current_line[1]
            local_json["packet_size"] = current_line[2]
            local_json["packet_id"] = current_line[0]
            local_json["time_stamp"] = get_timestamp(previous_line)
            nested_data=[]
            index = index + 1
            #continue_ = True
            try:
                while "Read:" not in lines[index] and "Send:" not in lines[index] and index < len(lines):
                    line = process_line(lines[index])
                    if len(line) > 1:
                        nested_data.append(line[1])
                    #nested_data.append(line[1] if len(line) > 0 else None)
                    #continue_ = True if "Read:" not in lines[index] and "Send:" not in lines[index] else False
                    #if continue_:
                    index = index + 1
                local_json["data"] = nested_data
                index = index - 1
                value_at = value_at + 1
            except:
                pass
            global_json.append(local_json)
        index = index + 1
    return global_json



def execution(file_name):
    lines = read_file(file_name)
    json_obj = parse_lines(lines)
    print(json_obj)


if __name__ == '__main__':
    fname = "./helpers/test_snoop_1.out"
    #fname = "test_snoop_.out"
    execution(fname)
    #test = process_line( ['1567527218348', 'Read:', '1448', 'bytes'])
