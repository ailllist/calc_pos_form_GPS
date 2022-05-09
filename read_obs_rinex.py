from copy import deepcopy

SIGNAL_LIST = ["C1", "L1", "C2", "P2", "L2", "C5", "L5"]

def split_signal(string: str) -> dict:
    signal_dict = {}
    signal_list = deepcopy(SIGNAL_LIST)

    tmp_line = ""
    for i in string:
        tmp_line += i
        if len(tmp_line) == 16:
            tmp_list = [tmp_line[:14], tmp_line[15]]
            signal_dict[signal_list[0]] = tmp_list
            del signal_list[0]
            tmp_line = ""

    return signal_dict

def split_sat(string: str) -> list:
    tmp_line = ""
    sat_list = []
    for i in string:
        tmp_line += i
        if len(tmp_line) == 3:
            sat_list.append(tmp_line)
            tmp_line = ""

    return sat_list

with open("suwn0320.15o") as f:
    lines = [i. strip("\n") for i in f.readlines()]
    HEADER = lines[:22]
    data = lines[22:]

loop = 0 # 2879
tot_sat_pos = {}

while True:

    tmp_dict = {}
    if data[1][:4] == "    ":
        info_of_data = data[:2]
        pre_data = info_of_data[0][30:]
        time_data = info_of_data[0][:27].strip()
        data_info = pre_data+data[1].strip()
        data_lines = 2

    else:
        info_of_data = data[0]
        time_data = info_of_data[:27].strip()
        data_info = info_of_data[30:]
        data_lines = 1

    sat_num = int(data_info[:2])
    tot_sat_str = data_info[2:]
    tot_sat = split_sat(tot_sat_str)

    rcv_data = data[data_lines:data_lines+sat_num*2] # GPS 수신기가 받은 데이터.
    for i in range(0, len(rcv_data), 2):
        while len(rcv_data[i+1]) != 32:
            rcv_data[i+1] += " "
        tot_line = rcv_data[i] + rcv_data[i+1]
        signal_dict = split_signal(tot_line)
        tmp_dict[tot_sat[0]] = signal_dict
        del tot_sat[0]

    tot_sat_pos[time_data] = tmp_dict
    data = data[data_lines+sat_num*2:] # 다음 데이터

    try:
        data_check = data[1]
    except:
        break
    loop += 1

if __name__ == "__main__":
    list_keys = list(tot_sat_pos.keys())
    for i in list_keys:
        print(i, tot_sat_pos[i])