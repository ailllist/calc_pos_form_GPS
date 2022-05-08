

with open("suwn0320.15o") as f:
    lines = [i. strip("\n") for i in f.readlines()]
    HEADER = lines[:22]
#
# for num, i in enumerate(HEADER):
#     print(num, i)

# 60번쨰 index부터 comment가 시작된다.

impact_line = HEADER[10]
print(impact_line)
comment = impact_line[60:]
data = impact_line[:60]
print(data)
print(comment)

comp_line = ""
for i in data:
    pass