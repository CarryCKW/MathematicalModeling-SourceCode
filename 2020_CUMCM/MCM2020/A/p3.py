import MCM2020.A.mcmutil as mu
import MCM2020.A.evaK as ek
import numpy as np
import MCM2020.A.evaK2 as ek2
import math
import random
import MCM2020.A.p2 as p2
import matplotlib.pyplot as plt


# 问题三代码

S = 1000000
Tempreatures = []
targetV = -1


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


beforetempdiff, beforeks, beforeres = ek2.getKsBeforePeek()
aftertempdiff, afterks, afterres = ek2.getKsAfterPeek()


def poll2(carv, temperatures):
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
        idx = ek2.place(carv, step)
        Ti = temperatures[idx - 1]
        Tn, k = ek2.tfunc(Ti, Tn_1, dalt, beforetempdiff, beforeks)
        x.append(dalt * step)
        y.append(Tn)
        step += 1
        Tn_1 = Tn
    temp = []
    Xplace = 0.5 * step * carv
    while Xplace <= allLen:
        Ti = 257 + (25 - 257) / 91 * (Xplace - 339.5)
        Tn, k = ek2.tfunc(Ti, Tn_1, dalt, aftertempdiff, afterks)
        x.append(dalt * step)
        y.append(Tn)
        if 340 <= Xplace <= 384:
            temp.append(k)
        step += 1
        Tn_1 = Tn
        Xplace = 0.5 * step * carv

    return x, y


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


def loops(times1, times2):
    global Tempreatures, S, targetV
    temp1 = np.linspace(165, 185, times1)
    temp2 = np.linspace(185, 205, times1)
    temp3 = np.linspace(225, 245, times1)
    temp4 = np.linspace(245, 265, times1)
    carvs = np.linspace(65, 100, times2)
    for i, ti1 in enumerate(temp1):
        for j, ti2 in enumerate(temp2):
            for k, ti3 in enumerate(temp3):
                for z, ti4 in enumerate(temp4):
                    for a, v in enumerate(carvs):
                        temperatures = [ti1, ti2, ti3, ti4, 25]
                        # print(temperatures)
                        # x, y = poll2(v, temperatures)
                        x, y = ek2.evaP1(temperatures, v)
                        t1, t2, T, p = getttT(x, y)
                        if p2.checkT1T2T(t1, t2, T):
                            print("ok t1, t2, T")
                            if targetMinSquare(x, y, v, p):
                                Tempreatures = temperatures
                            else:
                                continue

    print("min S:", S)
    print("diff tempers are:", Tempreatures)
    print("carV: " ,targetV)


def pools1(temperatures, times2):
    global Tempreatures
    diff = np.linspace(-10 ,10, 21)
    carvs = np.linspace(65/60, 100/60, times2)
    for idx, carv in enumerate(carvs):
        for i in range(diff.size):
            temps = []
            for j in range(4):
                temps.append(temperatures[j] + diff[i])
            temps.append(25)
            # print("temps:", temps)
            # print("carv:", carv)
            # x, y = poll2(carv, temps)
            x, y = ek2.evaP1(temperatures, carv)
            t1, t2, T, p = getttT(x, y)
            # print(t1, t2, T)
            if p2.checkT1T2T(t1, t2, T):
                # print("ok t1, t2, T")
                if targetMinSquare(x, y, carv, p):
                    print("success ont time.")
                    Tempreatures = temps
                else:
                    continue
    print("min S:", S)
    print("diff tempers are:", Tempreatures)
    print("carV: ", targetV)


def pools2(temperatures, times2):
    global Tempreatures
    diff = np.linspace(-7, 7, 15)
    carvs = np.linspace(65 / 60, 100 / 60, times2)
    for idx, carv in enumerate(carvs):
        for i in range(diff.size):
            temps = []
            for j in range(4):
                temps.append(temperatures[j] + diff[i] + np.random.randint(-3, 3))
            temps.append(25)
            x, y = ek2.evaP1(temperatures, carv)
            t1, t2, T, p = getttT(x, y)
            # print(t1, t2, T)
            if p2.checkT1T2T(t1, t2, T):
                # print("ok t1, t2, T")
                if targetMinSquare(x, y, carv, p):
                    print("success ont time.")
                    Tempreatures = temps
                else:
                    continue
        print("min S:", S)
        print("diff tempers are:", Tempreatures)
        print("carV: ", targetV)


def poolsALL(tempreatures, rge1, carvs, tub):
    global Tempreatures

    # tub = [185, 205, 245, 265]
    t1 = tempreatures[0]
    t2 = tempreatures[1]
    t3 = tempreatures[2]
    t4 = tempreatures[3]



    for idx, carv in enumerate(carvs):
        for ti1 in range(t1, tub[0], rge1):
            for ti2 in range(t2, tub[1], rge1):
                for ti3 in range(t3, tub[2], rge1):
                    for ti4 in range(t4, tub[3], rge1):
                        temperatures = [ti1, ti2, ti3, ti4, 25]
                        x, y = ek2.evaP1(temperatures, carv)
                        t1, t2, T, p = getttT(x, y)
                        if p2.checkT1T2T(t1, t2, T):
                            if targetMinSquare(x, y, carv, p):
                                Tempreatures  = temperatures
                            else:
                                continue


def poolALL2(times1, times2):
    global Tempreatures, S, targetV
    temp1 = np.linspace(165, 185, times1)
    temp2 = np.linspace(185, 205, times1)
    temp3 = np.linspace(225, 245, times1)
    temp4 = np.linspace(245, 265, times1)
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
                        if p2.checkT1T2T(t1, t2, T):
                            # print("ok t1, t2, T")
                            if targetMinSquare(x, y, v, p):
                                Tempreatures = temperatures
                            else:
                                continue

    print("min S:", S)
    print("diff tempers are:", Tempreatures)
    print("carV: ", targetV)


def poolwithLUB(times1, times2, t_lb, t_ub):
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
                        if p2.checkT1T2T(t1, t2, T):
                            # print("ok t1, t2, T")
                            if targetMinSquare(x, y, v, p):
                                Tempreatures = temperatures
                            else:
                                continue

    print("min S:", S)
    print("diff tempers are:", Tempreatures)
    print("carV: ", targetV)



if __name__ == '__main__':
    # temp1 = np.linspace(-10, 10, 21)
    # print(temp1)
    # loops(21, 36)
    temps = [165, 185, 225, 245, 25]
    tub = [185, 205, 245, 265]
    rge1 = 5
    carvs = np.linspace(65, 100, 36)
    # poolsALL(temps, rge1, carvs, tub)

    # poolALL2(4, 10)
    # print("finish :")
    # print("temps", Tempreatures)
    # print("carv:", targetV)
    # t_lb = [165, 185, 235, 245, 25]
    # t_ub = [185, 205, 245, 265, 25]
    t_lb = [176.3, 185, 229.66, 261, 25]
    t_ub = [180.33, 189, 233.66, 265, 25]
    # t_lb = [174.33, 187, 228.93, 261.0, 25]
    # t_ub = [178.64, 191, 232.93, 265, 25]
    # t_lb = [176.2, 190, 226.93, 263, 25]
    # t_ub = [179.2, 193, 130.93, 265.0, 25]
    poolwithLUB(4, 10, t_lb, t_ub)
    # print("finish : 更新temp划分区间的第一次迭代 (5, 10)")
    print("finish:")
    print("temps", Tempreatures)
    print("carv:", targetV)
    print("s: ", S)








