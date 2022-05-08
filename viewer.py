with open("suwn0320.15o") as f:
    lines = [i. strip("\n") for i in f.readlines()]
    HEADER = lines[:22]
    data = lines[22:]
    for num, i in enumerate(data):
        print(num, i)