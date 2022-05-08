with open("brdc0320.15n", "r") as f:
    lines = [i.strip("\n") for i in f.readlines()][8:]
    # PRN위성의 정보는 실질적으로 9번째 줄 (python은 index가 0부터 시작하기에)에 존재하므로
    # 9번째 줄부터 데이터를 읽어들인다. (슬라이싱)

res_lines = []
for i in lines:
    tmp_line = ''
    for num, j in enumerate(i):
        if num < len(i)-1:
            if i[num+1] == " " and j == " ":
                pass
            elif j == "-":
                if i[num-1] == "D":
                    tmp_line += j
                else:
                    tmp_line += " -"
            else:
                tmp_line += j
        else:
            tmp_line += j
    res_lines.append(tmp_line.strip())

epoch = len(res_lines)//8 # in this case = 411
tot_GPS = {} # 정렬을 PRN 기준으로 해야될 듯... time으로 하니까 생각이랑 다르게 특정 시간에 모든 PRN이 있지 않음.

for i in range(0, epoch):
    tmp_list = res_lines[8*i:(8*i)+8]
    res_list = []

    tmp_line = tmp_list[0]
    res_line = ""
    n_empty = 99 # PRN+epoch 구분 idx
    find_empty = True
    for num, j in enumerate(tmp_line): # 0번쩨 즐민 특별하게 가공함.
        if j == "." and find_empty:
            n_empty = num+2
            find_empty = False # PRN+epoch 구분 부분을 찾았기에 종료

        if num == n_empty:
            res_line += ","
        elif j == " " and tmp_line[num-4] == "D":
            res_line += ","
        else:
            res_line += j
    res_line = res_line.replace("D", "e")
    res_list.append(res_line.split(","))

    for k in tmp_list[1:]:
        tmp_line = ""
        for k1 in k:
            if k1 == " ":
                tmp_line += ","
            else:
                tmp_line += k1
        tmp_line = tmp_line.replace("D", "e")
        res_list.append(tmp_line.split(","))
    one_one = res_list[0][0].split(" ")
    PRN_info = str(one_one[0])

    try:
        pre_list = tot_GPS[PRN_info]
        pre_list.append(res_list)
        tot_GPS[PRN_info] = pre_list
    except:
        tot_GPS[PRN_info] = [res_list]