#!/usr/bin/python

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

def time_diff_with_string(time_s, time_e):
    return str(datetime.datetime.strptime(time_e, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(time_s, '%Y-%m-%d %H:%M:%S.%f'))

def time_diff_with_string_2(time_s, time_e):
    return datetime.datetime.strptime(time_e, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(time_s, '%Y-%m-%d %H:%M:%S.%f')

def time_add_with_string(time_s, time_e):
    return str(datetime.datetime.strptime(time_e, '%H:%M:%S.%f') + datetime.datetime.strptime(time_s, '%H:%M:%S.%f'))

def delta_addition(time_p, time_c):
    return (datetime.datetime.combine(datetime.date(1,1,1),time_p) + time_c).time()


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
            data_string = ""
            index = index + 1
            try:
                while "Read:" not in lines[index] and "Send:" not in lines[index] and index < len(lines):
                    line = process_line(lines[index])
                    if len(line) > 1:
                        data_string = data_string + line[1].strip().replace('.','')
                        #nested_data.append(line[1])
                    index = index + 1
                local_json["data_string"] = data_string.strip().replace('.','')
                local_json["data_array"] = nested_data
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
            data_string = ""
            index = index + 1
            try:
                while "Read:" not in lines[index] and "Send:" not in lines[index] and index < len(lines):
                    line = process_line(lines[index])
                    if len(line) > 1:
                        data_string = data_string + line[1]
                        #nested_data.append(line[1])
                    index = index + 1
                local_json["data_string"] = data_string.strip().replace('.','')
                local_json["data_array"] = ""
                index = index - 1
                value_at = value_at + 1
            except:
                pass
            global_json.append(local_json)
        index = index + 1
    return global_json

def extract_meta(_data):
    meta = {}
    send_count = 0
    read_count = 0
    bytes_sent = 0
    bytes_read = 0
    server_time = datetime.datetime.strptime("00:00:00.0000", '%H:%M:%S.%f').time()
    client_time = datetime.datetime.strptime("00:00:00.0000", '%H:%M:%S.%f').time()
    previous_packet = ""
    previous_timestamp = ""
    for x,packet in enumerate(_data):
        if x == 0:
            previous_packet = _data[0]["packet_type"]
            previous_timestamp = _data[0]["time_stamp"]
            if previous_packet == "Send:":
                send_count = send_count + 1
                bytes_sent = bytes_sent + int(packet["packet_size"])
            if previous_packet == "Read:":
                bytes_read = bytes_read + int(packet["packet_size"])
                read_count = read_count + 1
        else:
            if packet["packet_type"] == "Send:":
                send_count = send_count + 1
                bytes_sent = bytes_sent + int(packet["packet_size"])
                if previous_packet == "Send:":
                    difference = time_diff_with_string_2(previous_timestamp,packet["time_stamp"])
                    client_time = delta_addition(client_time,difference)
                    previous_timestamp = packet["time_stamp"]
                    previous_packet = "Send:"
                    continue
                if previous_packet == "Read:":
                    difference = time_diff_with_string_2(previous_timestamp,packet["time_stamp"])
                    server_time = delta_addition(server_time,difference)
                    previous_timestamp = packet["time_stamp"]
                    previous_packet = "Send:"
                    continue
            if packet["packet_type"] == "Read:":
                bytes_read = bytes_read + int(packet["packet_size"])
                read_count = read_count + 1
                if previous_packet == "Read:":
                    difference = time_diff_with_string_2(previous_timestamp,packet["time_stamp"])
                    server_time = delta_addition(server_time,difference)
                    previous_timestamp = packet["time_stamp"]
                    previous_packet = "Read:"
                    continue
                if previous_packet == "Send:":
                    difference = time_diff_with_string_2(previous_timestamp,packet["time_stamp"])
                    client_time = delta_addition(client_time,difference)
                    previous_timestamp = packet["time_stamp"]
                    previous_packet = "Read:"
                    continue
    meta["client_time"] = str(client_time)
    meta["server_time"] = str(server_time)
    meta["send_count"] = send_count
    meta["read_count"] = read_count
    meta["bytes_sent"] = bytes_sent
    meta["bytes_read"] = bytes_read
    meta["start_time"] = _data[0]["time_stamp"]
    meta["end_time"] = _data[-1]["time_stamp"]
    meta["total_duration"] = time_diff_with_string(meta["start_time"],meta["end_time"])
    meta["uploaded_at"] = str(datetime.datetime.now())
    #print("Server time:{} Client time: {} Total time: {}".format(server_time,client_time,meta["total_duration"]))
    return meta

def execution(file_name):
    lines = read_file(file_name)
    data_json = parse_lines(lines)
    statistics = extract_meta(data_json)
    f_line = lines[0]
    lines=""
    if "=" and ":" in f_line:
        statistics["server_url"]= f_line.split('=')[-1].split(':')[0]
        statistics["port_number"]= f_line.split('=')[-1].split(':')[-1]
    file = open('./helpers/temp_snoop.json', 'w')
    file.write(json.dumps(data_json))
    file.close()
    return True, statistics

'''
if __name__ == '__main__':
    #fname = "./helpers/test_snoop_1.out"
    fname = "test_snoop_1.out"
    #execution(fname)
    lines = read_file(fname)

    data_json = parse_lines(lines)
    statistics = extract_meta(data_json)
    f_line = lines[0]
    lines =""
    if "=" and ":" in f_line:
        statistics["server_url"]= f_line.split('=')[-1].split(':')[0]
        statistics["port_number"]= f_line.split('=')[-1].split(':')[-1]
    print(statistics)
'''
