import MCM2020.A.mcmutil as mu
import MCM2020.A.evaK as ek
import numpy as np
import matplotlib.pyplot as plt


#wrong version


# datafile = r'C:\Users\蔡小蔚\Desktop\2020\A\dataA.xlsx'
# res = mu.excel_to_matrix(datafile, False)
#
# print(res.shape)
#
# x = res[:, 0]
# y = res[:, 1]

tempatures = [173, 198, 230, 257, 25]
xx, yy = ek.getKlist()
xx, yy = ek.completeAllKs2(xx, yy)
# print(xx)
# print(yy)
# print(len(xx))

def getAlphaWhenMinIndex(x, y, tempnow):
    index = 0
    minSub = 100
    # size = x.shape[0]
    size = len(x)
    for i in range(size):
        tempSub = abs(x[i] - tempnow)
        if tempSub < minSub:
            minSub = tempSub
            index = i

    return y[index]


def place(carv, step):
    lentemp = 0.5*step*carv
    if lentemp<=197.5:
        return 1
    if lentemp<=233:
        return 2
    if lentemp<=268.5:
        return 3
    if lentemp<=339.5:
        return 4
    return 5



lenAll = 435.5
carv = 1.3
timaAll = lenAll / carv
step = 0
timelist = []
tempaturelist = []
steplist = []
T0 = 25
dalt = 0.5
while 0.5*step*carv<=lenAll:
    k = getAlphaWhenMinIndex(xx, yy, T0)
    idx = place(carv, step)
    Ti = tempatures[idx - 1]
    T = Ti - (Ti - T0)*np.exp(-k*0.5)
    steplist.append(step)
    tempaturelist.append(T)
    T0 = T
    step+=1
    timelist.append(step*dalt)


print("time:", timelist)
print("tempreature: ", tempaturelist)

filepathTimeList = "timelist.txt"
filepathTempreatureList = "templist.txt"
print("size:", len(timelist))
mu.WriteFile(timelist, filepathTimeList)
mu.WriteFile(tempaturelist, filepathTempreatureList)


plt.plot(timelist, tempaturelist)
plt.xlabel("Time (s) ")
plt.ylabel("Circuit Board's Temperature  (°C)")
plt.show()


print(tempaturelist)