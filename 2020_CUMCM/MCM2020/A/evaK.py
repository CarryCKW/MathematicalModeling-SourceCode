import MCM2020.A.mcmutil as mu
import matplotlib.pyplot as plt
import numpy as np


# res = mu.excel_to_matrix(datafile, False)
# x = res[:, 0]
# y = res[:, 1]
#
# # print(mu.checkAllInsercUntil(y))
#
#
# res = mu.getKsAtTimePoints2(x, y,None, None)



def completeAllKs2(x, y):
    daltX = 0.5
    daltY = 0.0003
    while x[0]>25:
        x.insert(0, x[0] - daltX)
        y.insert(0, y[0] - daltY)

    return x, y


# i = 0
# xx = []
# yy = []
# # print(res)
# for itt in res.items():
#     if -0.5<itt[1]<0.5:
#         xx.append(itt[0])
#         yy.append(itt[1])
#
#
# xx, yy = completeAllKs2(xx, yy)
# plt.plot(xx, yy)
# plt.xlabel("Circuit board's Temperature (°C)")
# plt.ylabel("αA/pvc ")
# plt.show()


def getKlist():
    datafile = r'...'
    res = mu.excel_to_matrix(datafile, False)
    x = res[:, 0]
    y = res[:, 1]
    res = mu.getKsAtTimePoints2(x, y, None, None)

    xx = []
    yy = []
    # print(res)
    for itt in res.items():
        if -0.5 < itt[1] < 0.5:
            xx.append(itt[0])
            yy.append(itt[1])
    return xx, yy


def getIndex(x, y, temp):
    size = x.shape[0]
    index = 0


def checkK():
    sectionTimeOfEnd = [296, 373]
    Ti = 25
    timex = np.linspace(sectionTimeOfEnd[0], sectionTimeOfEnd[1], (373-296)*2)


def completeAllKs(x, y):
    size = len(x)
    N = 20
    newX = []  #means diff new tempreature added before the old
    newY = []  #means diff new k added before the old
    temp = 30.03
    index = 0
    while temp>25:
        j = index
        sumK = 0
        for i in range(N):
            sumK += y[j]
            j+=1
        daltK = sumK/N
        # newX.append(temp)
        # newY.append(y[index] - daltK)
        # newX.index(temp, 0)
        x.insert(temp, 0)
        y.insert(y[index] - daltK, 0)
        # temp = ?


#画出alpha图片
def draw():
    datafile = r'C:\Users\蔡小蔚\Desktop\2020\A\dataA.xlsx'
    res = mu.excel_to_matrix(datafile, False)
    x = res[:, 0]
    y = res[:, 1]
    res = mu.getKsAtTimePoints2(x, y, None, None)
    # tempdiff, ks, res = mu.getKsTempDiff(x, y, None, None)
    i = 0
    xx = []
    yy = []
    # print(res)
    for itt in res.items():
        # if -0.5 < itt[1] < 0.5:
            xx.append(itt[0])
            yy.append(itt[1])

    xx, yy = completeAllKs2(xx, yy)
    # plt.plot(xx, yy)
    plt.scatter(xx, yy, marker='*', s=1)
    plt.xlabel("Circuit board's Temperature (°C)")
    plt.ylabel("αA/pvc ")
    plt.show()


section = [0, 180, 210, 240, 300]


#画出dlatTempreature与K的关系图
def getKsWithTempDiff():
    datafile = r'...'
    res = mu.excel_to_matrix(datafile, False)
    x = res[:, 0]
    y = res[:, 1]
    tempdiff, ks, res = mu.getKsTempDiffAfterPeek(x, y, None, None)
    plt.scatter(tempdiff, ks, marker='*', s=1)
    plt.xlabel("diff Tempreature")
    plt.ylabel("K")
    plt.show()


def drawWenqu(tempatres, carv, dalta):
    tempatres = [25, 175, 195, 235, 255, 25]
    section = [25, 197.5, 202.5, 233, 238, 268.5, 273.5, 339.5, 430.5]
    len = 430.5
    # timedata = np.linspace(0, len/carv, 200)
    timedata  = [i for i in range(1000)]
    # print(timedata)
    k = []
    k.append((tempatres[1] - tempatres[0])/25)
    k.append((tempatres[2] - tempatres[1])/5)
    k.append((tempatres[3] - tempatres[2])/5)
    k.append((tempatres[4] - tempatres[3])/5)
    k.append((tempatres[5] - tempatres[4])/91)
    y = []
    for i, ti in enumerate(timedata):
        x = carv*ti
        if 0<=x<section[0]:
            f = k[0]*x + tempatres[0]
            y.append(f)
        if section[0]<=x<section[1]:
            y.append(tempatres[1])
        if section[1]<=x<section[2]:
            f = tempatres[1]+k[1]*(x - section[1])
            y.append(f)
        if section[2]<=x<section[3]:
            y.append(tempatres[2])
        if section[3]<=x<section[4]:
            f = tempatres[2] + k[2]*(x - section[3])
            y.append(f)
        if section[4]<=x<section[5]:
            y.append(tempatres[3])
        if section[5]<=x<section[6]:
            f = tempatres[3] + k[3]*(x - section[5])
            y.append(f)
        if section[6]<=x<section[7]:
            y.append(tempatres[4])
        if section[7]<=x<=section[8]:
            f = tempatres[4] + k[4]*(x - section[7])
            y.append(f)
        if x>section[8]:
            y.append(0)
    realx = []
    realy = []
    for i in range(timedata.__len__()):
        if y[i]!=0:
            realx.append(timedata[i])
            realy.append(y[i])
    return realx, realy



#画出案例图像
def drawAnli():
    datafile = r'...'
    res = mu.excel_to_matrix(datafile, False)
    timedata, orignY = drawWenqu(None, 7/6, 0.5)

    x = res[:, 0]
    y = res[:, 1]

    print("x_size", len(x))
    print("timedata_size ", len(timedata))

    maxdiff = -1
    for i, ti in enumerate(timedata):
        Ti = orignY[i]
        T0 = y[ti]
        maxdiff = max(maxdiff, abs(Ti - T0))
    print("maxdiff:", maxdiff)
    plt.plot(x, y,label = "reflow profile", linewidth = 1)
    plt.plot(timedata, orignY, label = "stove tempreature", linewidth = 1 )
    plt.xlabel("Time (s)")
    plt.ylabel("Tempreature  (°C)")
    plt.legend()
    plt.show()


#[25, 280]
# def getKsByDaltaTempre(dt, ):



if __name__ == '__main__':
    getKsWithTempDiff()
    # drawAnli()