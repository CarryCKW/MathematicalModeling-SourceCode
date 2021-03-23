import MCM2020.A.mcmutil as mu
import MCM2020.A.evaK as ek
import numpy as np
import MCM2020.A.evaK2 as ek2
import math
import random
import MCM2020.A.p2 as p2
import matplotlib.pyplot as plt


# 问题四代码

S = 410
deltaS = 10   # S - delta < S' < S + delta
Tempreatures = []
targetV = -1
sumMSE = 100000


def targetMinSumOfMSE(x, y, temps, carv):
    global sumMSE, Tempreatures, targetV
    T, idx, p1 = getTI(x, y)
    thisMSE = 0
    while p1<idx:
        diffp = abs(idx - p1)
        p2 = idx + diffp
        (xp2, yp2) = (x[p2], y[p2])
        thisMSE += (yp2 - y[p1])**2
        p1 += 1
    print("thisMSE: ", thisMSE)
    if thisMSE<sumMSE:
        sumMSE = thisMSE
        Tempreatures = temps
        targetV = carv
        print("now sumOfMSE: ", sumMSE)
        print("now Tempreatures", Tempreatures)
        print("targetV: ", targetV)


def getTI(x, y):
    T = -1
    index = -1
    p1 = 0
    findS = False
    for idx, ti in enumerate(y):
        if findS == False and ti>=217:
            p1 = idx
            findS = True
        if ti > T:
            T = ti
            index = idx
    return T, index, p1


def checkLTRWhen217(x, y, dtlen):
    li = 0
    ri = 0
    findL = False
    findR = False
    T = -1
    index = -1
    for idx, ti in enumerate(y):
        if T < ti:
            T = ti
            index = idx
        if ti>=217 and findL==False:
            li = idx
            findL = True
        if ti<217 and findR==False and findL==True:
            ri = idx

    dt1 = abs(x[index] - x[li])
    dt2 = abs(x[ri] - x[index])
    # print("dt1 - dt2:", abs(dt1 - dt2))
    return abs(dt1 - dt2) <= dtlen


def getttT(x, y):
    timestart = -1
    timeend = -1
    t1 = 0  # 温度上升过程中在150ºC~190ºC的时间
    t2 = 0  # 温度大于217ºC的时间
    T = 0  # 峰值温度
    size = x.__len__()

    findS1 = False
    findE1 = False
    findS2 = False
    findE2 = False
    p1=p2=p3=p4 = 0
    for i in range(size):
        if y[i]>T:
            T = y[i]
            p5 = i
        if y[i]>=150 and findS1==False:
            p1 = i
            findS1 = True
        if y[i]>=190 and findE1 == False and findS1==True:
            p2 = i
            findE1 = True
        if y[i]>=217 and findS2 == False:
            p3 = i
            findS2 = True
        if y[i]<217 and findE2 == False and findS2==True :
            p4 = i
            findE2 = True
            break
    t1 = abs(x[p1] - x[p2])
    t2 = abs(x[p3] - x[p4])
    return t1, t2, T, p5


def checkSquare(x, y, carv, p):
    p1 = 0
    p2 = p
    for i, t in enumerate(y):
        if y[i] >= 217:
            p1 = i
            break
    square = 0
    delat = 0.5
    s0 = (p2 - p1) * delat * y[p1]
    while p2 > p1:
        pnext = p1 + 1
        square += (y[pnext] + y[p1]) / 2 * delat
        p1 += 1
    square -= s0
    global S, deltaS
    if abs(S - square)<deltaS:
        return True
    return False


def targetMinSquare(x, y, carv, p):
    p1 = 0
    p2 = p
    for i, t in enumerate(y):
        if y[i]>=217:
            p1 = i
            break
    square = 0
    delat = 0.5
    s0 = (p2 - p1)*delat*y[p1]
    while p2>p1:
        pnext = p1 + 1
        square += (y[pnext] + y[p1])/2*delat
        p1+=1
    square-=s0
    # print("square:", square)
    global S
    global targetV
    if square < S:
        S = square
        targetV = carv
        print("now S=", S)
        print("temp:", Tempreatures)
        print("now targetV:",targetV)
        return True
    return False


def poolwithLUB(times1, times2, t_lb, t_ub, dtlen):
    global Tempreatures, S, targetV
    temp1 = np.linspace(t_lb[0], t_ub[0], times1)
    temp2 = np.linspace(t_lb[1], t_ub[1], times1)
    temp3 = np.linspace(t_lb[2], t_ub[2], times1)
    temp4 = np.linspace(t_lb[3], t_ub[3], times1)
    carvs = np.linspace(65/60, 100/60, times2)
    for i, ti1 in enumerate(temp1):
        for j, ti2 in enumerate(temp2):
            for k, ti3 in enumerate(temp3):
                for z, ti4 in enumerate(temp4):
                    for a, v in enumerate(carvs):
                        temperatures = [ti1, ti2, ti3, ti4, 25]
                        x, y = ek2.evaP1(temperatures, v)
                        t1, t2, T, p = getttT(x, y)
                        # print(t1, t2, T)
                        if checkSquare(x, y, v, p) and p2.checkT1T2T(t1, t2, T):
                            # print("ok t1, t2, T")
                            targetMinSumOfMSE(x, y, temperatures, v)


    print("min S:", S)
    print("diff tempers are:", Tempreatures)
    print("carV: ", targetV)




if __name__ == '__main__':
    # t_lb = [165, 185, 235, 245, 25]
    # t_ub = [185, 205, 245, 265, 25]

    # t_lb = [176.3, 185, 229.66, 261, 25]
    # t_ub = [180.33, 189, 233.66, 265, 25]
    # t_lb = [174.33, 187, 228.93, 261.0, 25]
    # t_ub = [178.64, 191, 232.93, 265, 25]
    # t_lb = [176.2, 190, 226.93, 263, 25]
    # t_ub = [179.2, 193, 130.93, 265.0, 25]

    t_lb = [165, 185, 238.667, 261, 25]
    t_ub = [169, 189, 244.667, 265, 25]

    dtlen = 0
    poolwithLUB(4, 10, t_lb, t_ub, dtlen)
    print("finish:")
    print("temps", Tempreatures)
    print("carv:", targetV)
    print("s: ", S)
    print("sumMSE:", sumMSE)

