strs = ["  25033584.828 5 131552383.410 5  25033598.742 5  25033596.98045 102508399.25245", "  25033598.297 7  98237194.127 7"]
# strs = ["  25033584.828 5                  25033598.742 5  25033596.98045 102508399.25245", "  25033598.297 7  98237194.127 7"]

# C1    L1    C2    P2    L2    C5    L5순
# data의 특징... 정수부 9자리 + 소수부 3자리 = 12자리 다만, C1 데이터의 경우 정수부를 8자리로 봐도 될 것 같긴한데...
# 줄 의 맢에는 2자리씩 띄는 경향이 있는듯?

tot_str = strs[0] + strs[1]

signal_dict = {}
signal_list = ["C1", "L1", "C2", "P2", "L2", "C5", "L5"]
print(tot_str)

tmp_line = ""
for i in tot_str:
    tmp_line += i
    if len(tmp_line) == 16:
        tmp_list = [tmp_line[:14], tmp_line[15]]
        signal_dict[signal_list[0]] = tmp_list
        del signal_list[0]
        tmp_line = ""

print(signal_dict)