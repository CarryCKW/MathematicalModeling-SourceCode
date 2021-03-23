import MCM2020.A.mcmutil as mu
import MCM2020.A.evaK as ek
import numpy as np
import MCM2020.A.evaK2 as ek2
import math
import random


#问题二代码

targetV = -1
minf = -targetV + 1000*3
M = 1
Vs = []

beforetempdiff, beforeks, beforeres = ek2.getKsBeforePeek()
aftertempdiff, afterks, afterres = ek2.getKsAfterPeek()


def checkT1T2T(t1, t2, T):
    if 60<=t1<=120 and 40<=t2<=90 and 240 <=T <= 250:
        return True
    return False


def targetValue(v, t1, t2, T):
    tempt1 = ((min(0, 120 - t1))**2 + (min(0, t1 - 60))**2)*M
    tempt2 = (M*(min(0, 90 - t2))**2 + (min(0, t2 - 40))**2)*M
    tempT = (M*(min(0, 250 - T))**2 + (min(0, T - 240))**2)*M
    if checkT1T2T(t1, t2, T):
        global Vs
        Vs.append(v)
    tempminf = -v + tempt1 + tempt2 + tempT
    global targetV
    global minf
    if tempminf<=minf:
        minf = tempminf
        targetV = v


#以下穷举
def poll(carv, tempreatures):
    dalt = 0.5
    allLen = 435.5
    tempreatures = [182, 203, 237, 254, 25]
    x, y = ek2.evaP1(tempreatures, carv)
    assert x.__len__() == y.__len__()
    timestart = -1
    timeend = -1
    t1 = 0 #温度上升过程中在150ºC~190ºC的时间
    t2 = 0 #温度大于217ºC的时间
    T = 0 #峰值温度
    size = x.__len__()

    findS = False
    findE = False
    for i in range(size):
        if y[i]>=150 and findS==False:
            timestart = x[i]
            findS = True
        if y[i]>=190 and findE == False:
            timeend = x[i]
            findE = True
            break
    t1 = abs(timeend - timestart)

    findS = False
    findE = False
    for i in range(size):
        T = max(T, y[i])
        if y[i] >= 217 and findS == False:
            timestart = x[i]
            findS = True
        if y[i] <217 and findE == False and findS == True:
            timeend = x[i]
            findE = True
            break
    t2 = abs(timeend - timestart)

    return t1, t2, T


def loop(times):
    carvs = np.linspace(65 / 60, 100 / 60, times)
    size = carvs.size
    # print(carvs)
    tempreatures = [182, 203, 237, 254, 25]
    for i in range(size):
        carv = carvs[i]
        t1, t2, T = poll(carv, tempreatures)
        targetValue(carv, t1, t2, T)


#以下为模拟退火
def func(v):
    t1, t2, T = poll(v)
    tempt1 = ((min(0, 120 - t1)) ** 2 + (min(0, t1 - 60)) ** 2) * M
    tempt2 = ( (min(0, 90 - t2)) ** 2 + (min(0, t2 - 40)) ** 2) * M
    tempT = ((min(0, 250 - T)) ** 2 + (min(0, T - 240)) ** 2) * M
    tempminf = -v + tempt1 + tempt2 + tempT
    return tempminf


def SA():
    narvs = 1
    T0 = 25
    T = 100
    Tmin = 30
    maxgen = 500
    Lk = 200
    alfa = 0.8
    v_lb = 65/60
    v_ub = 100/60
    x0 = v_lb + (v_ub - v_lb)*np.random.random(1)
    x = x0
    y = func(x0)
    results = []
    while T>Tmin:
        x_best = x
        y_best = y
        flag = 0
        for i in range(100):
            delta_x = random.random() - 0.5
            if v_lb < (x+delta_x) < v_ub:
                x_new = x+delta_x
            else:
                x_new = x - delta_x
            y_new = func(x_new)
            print("y=", y)
            print("y_new=", y_new)
            print("T=", T)
            if y_new < y or np.exp(-(y - y_new)/T) > random.random():
                flag = 1
                x = x_new
                y = y_new
                if y < y_best:
                    x_best = x
                    y_best = y
        if flag:
            x = x_best
            y = y_best
        results.append((x, y))
        T *= alfa
    print("最优解:", results[-1])




if __name__ == '__main__':
    loop(1000)
    print("targetV:", targetV)
    maxv = -1
    for i, v in enumerate(Vs):
        maxv = max(maxv, v)
    print("maxV: ", maxv)
    # SA()