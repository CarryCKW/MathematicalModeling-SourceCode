import MCM2020.A.evaK as ek
import MCM2020.A.mcmutil as mu
import matplotlib.pyplot as plt
import numpy as np
import math


#问题一代码

# 补全x, y data
def completeXY(x, y):
    datax = 0.5
    datay = 0.5
    while y[0] >= 25.5:
        x.insert(0, x[0] - datax)
        y.insert(0, y[0] - datay)
    return x, y


def getKsBeforePeek():
    datafile = r'...'
    res = mu.excel_to_matrix(datafile, False)
    # timedata, orignY = ek.drawWenqu(None, 7 / 6, 0.5)
    x = res[:, 0]
    y = res[:, 1]
    x = list(x)
    y = list(y)
    x, y = completeXY(x, y)
    x = np.array(x)
    y = np.array(y)
    # print(y)
    tempdiff, ks, res = mu.getKsTempDiffBeforePeek(x, y, None, None)
    # print(tempdiff)
    # print(ks)
    # print(res)
    # plt.scatter(tempdiff, ks, marker='*', s=1)
    # plt.xlabel("temperature difference  ( °C )")
    # plt.ylabel("αA / pvc")
    # plt.show()
    return tempdiff, ks, res


def getKsAfterPeek():
    datafile = r'...'
    res = mu.excel_to_matrix(datafile, False)
    # timedata, orignY = ek.drawWenqu(None, 7 / 6, 0.5)
    x = res[:, 0]
    y = res[:, 1]
    x = list(x)
    y = list(y)
    x, y = completeXY(x, y)
    x = np.array(x)
    y = np.array(y)
    # print(y)
    tempdiff, ks, res = mu.getKsTempDiffAfterPeek(x, y, None, None)
    # print(tempdiff)
    # print("ks:",ks)
    # print(res)
    # plt.scatter(tempdiff, ks, marker='*', s=1)
    # plt.xlabel("temperature difference  ( °C )")
    # plt.ylabel("αA / pvc")
    # plt.show()
    return tempdiff, ks, res


def getKwithSimilarDT(x, y, dtnow):
    index = 0
    minSub = 100
    # size = x.shape[0]
    size = len(x)
    for i in range(size):
        tempSub = abs(x[i] - dtnow)
        if tempSub < minSub:
            minSub = tempSub
            index = i
    # if y[index]-0.000001<0.0:
    #     print("point at ", index)
    return y[index]


def tfunc(Ti, T0, dalt, x, y):
    a = Ti - T0
    k = getKwithSimilarDT(x, y, a)
    T = Ti - a * np.exp(-k * dalt)
    # if k==0:
    #     print("yes")
    return T, k


def place(carv, step):
    lentemp = 0.5 * step * carv
    if lentemp <= 197.5:
        return 1
    if lentemp <= 233:
        return 2
    if lentemp <= 268.5:
        return 3
    if lentemp <= 339.5:
        return 4
    return 5


def evaP1(tempreatures, carv):
    beforetempdiff, beforeks, beforeres = getKsBeforePeek()
    aftertempdiff, afterks, afterres = getKsAfterPeek()
    # print(beforeks)
    Tn_1 = 25
    dalt = 0.5
    allLen = 435.5
    # tempreatures = [173, 198, 230, 257, 25]
    Tn = 30
    # carv = 1.3
    step = 0
    x = []
    y = []
    idx = 0
    while idx < 5:
        idx = place(carv, step)
        Ti = tempreatures[idx - 1]
        Tn, k = tfunc(Ti, Tn_1, dalt, beforetempdiff, beforeks)
        x.append(dalt * step)
        y.append(Tn)
        step += 1
        Tn_1 = Tn
    temp = []
    Xplace = 0.5*step*carv
    while Xplace <= allLen:
        Ti = 257 + (25 - 257)/91 * (Xplace - 339.5)
        Tn , k = tfunc(Ti, Tn_1, dalt, aftertempdiff, afterks)
        x.append(dalt * step)
        y.append(Tn)
        if 340 <=Xplace <=384:
            temp.append(k)
        step += 1
        Tn_1 = Tn
        Xplace = 0.5*step*carv

    return x, y
    # filepathTimeList = "timelist.txt"
    # filepathTempreatureList = "templist.txt"
    # mu.WriteFile(x, filepathTimeList)
    # mu.WriteFile(y, filepathTempreatureList)

    # plt.plot(x, y)
    # plt.xlabel("time ( s ) ")
    # plt.ylabel("Circuit board's Temperature ( °C )")
    # plt.show()


def evaT1T2T(x, y):
    timestart = -1
    timeend = -1
    t1 = 0  # 温度上升过程中在150ºC~190ºC的时间
    t2 = 0  # 温度大于217ºC的时间
    T = 0  # 峰值温度
    size = x.__len__()

    findS = False
    findE = False
    for i in range(size):
        if y[i] >= 150 and findS == False:
            timestart = x[i]
            findS = True
        if y[i] >= 190 and findE == False:
            timeend = x[i]
            findS = True
            break
    t1 = abs(timeend - timestart)

    findS = False
    findE = False
    for i in range(size):
        T = max(T, y[i])
        if y[i] >= 217 and findS == False:
            timestart = x[i]
            findS = True
        if y[i] < 217 and findE == False and findS == True:
            timeend = x[i]
            findS = True
            break
    t2 = abs(timeend - timestart)
    return t1, t2, T


if __name__ == '__main__':
    # tempdiff, ks, res = getKsAfterPeek()
    # print(tempdiff)
    # print(getKwithSimilarDT(tempdiff, ks, 140))
    tempreatures = [173, 198, 230, 257, 25]
    temp2 = [165.0, 185.0, 225.0, 245.0, 25]
    temp3 = [176.3, 189, 230.933, 265, 25]
    temp4 = [182, 203, 237, 254, 25]
    temp5 = [165.0, 187.66666666666666, 238.667, 265.0, 25]
    carv5 = 1.407407
    carv4 = 1.2207421
    carv3 = 1.407
    carv2 = 1.1835
    carv = 1.3
    # x, y = evaP1(tempreatures, carv)
    x, y = evaP1(temp5, carv5)
    t1, t2, T = evaT1T2T(x, y)
    print("t1:", t1)
    print("t2:", t2)
    print("T:", T)
    plt.scatter(x, y, s=1, label='Temperature-Time')
    plt.axvline(241.3, color='coral', label='x time = 241.3s')
    plt.axhline(217, color = '#664E00', label='217°C')
    t1, t2, T = evaT1T2T(x, y)
    print(t1, t2, T)
    plt.xlabel("time ( s ) ")
    plt.ylabel("Circuit board's Temperature ( °C )")
    plt.legend()
    plt.show()
