input6 = [[1,1],[1,2]]
input3 = [[1,0,0,1,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,1]]
input4 = [[1,0,0,0,0,0,0,0,0,0]]
res = 0

tp = 0
for i in input6:
    a = input4[i[0]-1]
    b = input3[i[1]-1]


    for j in range(len(a)):
        if a[j] == 1 and b[j] == 1:
            tp += 1


print(tp)