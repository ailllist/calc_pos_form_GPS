import time

s_time = time.time()
with open("suwn0320.15o") as f:
    lines = [i. strip("\n") for i in f.readlines()]
    HEADER = lines[:22]
    data = lines[22:]
loop = 0 # 2879

while True:
    if data[1][:4] == "    ":
        info_of_data = data[:2]
        pre_data = info_of_data[0][30:]
        data_info = pre_data+data[1].strip()
        data_lines = 2
        
    else:
        info_of_data = data[0]
        data_info = info_of_data[30:]
        data_lines = 1
        
        
    print(f"before_int : {data_info[:2]}, lines : {data_lines}, data : {info_of_data}, loop : {loop}")
    
    sat_num = int(data_info[:2])
    tot_sat_str = data_info[2:]
    tot_sat = []
    cnt = 0
    tmp_line = ""
    while cnt != len(tot_sat_str):
        tmp_line += tot_sat_str[cnt]
        if len(tmp_line) == 3:
            tot_sat.append(tmp_line)
            tmp_line = ""
        cnt += 1
    rcv_data = data[data_lines:data_lines+sat_num*2]
    for num, i in enumerate(data[:data_lines+sat_num*2]):
        print(num, i)
    #for num, i in enumerate(rcv_data):
    #    print(num, i)
    try:
        data = data[data_lines+sat_num*2:]
    except:
        break
    loop += 1
print(time.time()-s_time)