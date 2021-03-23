from io import open
import glob
import numpy as np
import math
import os
import xlrd
from sklearn import preprocessing
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
from scipy.optimize import curve_fit


#写入文件
def WriteFile(arr, filePath):
    np.savetxt(filePath, arr, fmt="%.2f")


#读取excel
def excel_to_matrix(path, need1line=False):
    table = xlrd.open_workbook(path).sheets()[0]  # 获取第一个sheet表
    row = table.nrows  # 行数
    if need1line == False:
        row -=1
    col = table.ncols  # 列数
    datamatrix = np.zeros((row, col))  # 生成一个nrows行ncols列，且元素均为0的初始矩阵
    for x in range(col):
        # if x == 0:
        #     continue
        cols = np.array(table.col_values(x))  # 把list转换为矩阵进行矩阵操作
        if need1line==False:
            cols = cols[1:]
        datamatrix[:, x] = cols  # 按列把数据存进矩阵中
    return datamatrix
    # # 数据归一化
    # min_max_scaler = preprocessing.MinMaxScaler()
    # datamatrix = min_max_scaler.fit_transform(datamatrix)
    # return datamatrix


def checkUpOrDown(tn_1, temperautren_1, tn, temperaturen):
    tempres = (temperaturen - temperautren_1)/(tn - tn_1)
    if abs(tempres)>3:
        return False
    return True


def caluateTimeBetween150_190(temperautre):
    return 150 <= temperautre <= 190


def caluateTimeUp217(temperautre):
    return temperautre>=217


def checkPeek(tempy):
    size = tempy.shape[0]
    peek = -1
    for i in range(size):
        peek = max(peek, tempy[i])
    if 240 <= peek <= 250:
        return True
    else:
        return False


def checkAllInsercUntil(tempy):
    size = tempy.shape[0]
    for i in range(size):
        if i==0:
            continue
        if tempy[i] < tempy[i-1] :
            return i

    return -1


def getSectionWithUP(tempy):
    s = 1
    e = checkAllInsercUntil(tempy)
    k = tempy[1] - tempy[0]
    res = []
    for i in range(s, e):
        diff = tempy[i+1] - tempy[i]
        if diff > k:
            res.append(i)
            k = diff

    return res


def func(x, a, b, c):
    return -a*np.exp(-b*x) + c


def getK(Ti, T0, s, e, x, y):
    x = x[s:s+e]
    y = y[s:s+e]
    res = []
    popt, pcov = curve_fit(func, x, y)
    k = popt[1]
    a = popt[0]
    c = popt[2]
    print(a, k, c)
    xdata = np.linspace(0,180, 360)
    y2 = [func(i, a, k, c) for i in xdata]
    plt.plot(xdata, y2)
    plt.show()
    return k


def getAllArgs(Ti, T0, s, e, x, y):
    x = x[s:s + e]
    y = y[s:s + e]
    resk = []
    resTi = []
    resA = []
    popt, pcov = curve_fit(func, x, y)
    k = popt[1]
    a = popt[0]
    c = popt[2]
    return a, k, c


def getKAtOnePoint(T, Ti, T0, diat):
    a = Ti - T0
    c = Ti
    k = -(np.log((c - T)/a))/diat
    return k


def getKsAtTimePoints(x, y):
    size = x.shape[0]
    res = {}
    tempatres = [175, 195, 235, 255]
    section = [0, 169, 200, 230, 295]
    diat = 0.5
    for i in range(size):
        if i == 0:
            continue
        if section[0]<=x[i]<section[1]:
            Ti = tempatres[0]
            res[y[i]] = getKAtOnePoint(y[i], Ti, y[i-1], diat)
        if section[1]<=x[i]<section[2]:
            Ti = tempatres[1]
            res[y[i]] = getKAtOnePoint(y[i], Ti, y[i-1], diat)
        if section[2]<=x[i]<section[3]:
            Ti = tempatres[2]
            res[y[i]] = getKAtOnePoint(y[i], Ti, y[i - 1], diat)
        if section[3]<=x[i]<=section[4]:
            Ti = tempatres[3]
            res[y[i]] = getKAtOnePoint(y[i], Ti, y[i - 1], diat)

    return res


def getSubsectionTempature(tempatres, section, index, dx, x):
    place = [147.5, 233, 268.5, 339.5]
    tempatres = [175, 195, 235, 255, 25]
    section = [25, 197.5, 202.5, 233, 238, 268.5, 273.5, 339.5, 430.5]

    if index == 1:
        k = (tempatres[index] - tempatres[index - 1])/dx
        res = k*(x - section[1]) + tempatres[0]
        return res
    if index == 2:
        k = (tempatres[index] - tempatres[index - 1]) / dx
        res = k * (x - section[3]) + tempatres[1]
        return res
    if index == 3:
        k = (tempatres[index] - tempatres[index - 1]) / dx
        res = k * (x - section[5]) + tempatres[2]
        return res
    if index == 4:
        k = (tempatres[index] - tempatres[index - 1]) / dx
        res = k * (x - section[7]) + tempatres[3]
        return res



def getKsAtTimePoints2(x, y, tempatres, section):
    tempatres = [175, 195, 235, 255, 25]
    tempatres2 = [185, 205, 245, 265, 25]
    section = [0, 147.5, 200, 230, 295]
    size = x.shape[0]
    res = {}
    diat = 0.5
    dx = 5
    sectionOfTime = [0, 169, 173.5, 199.6, 204, 230, 234, 291, 295, 351.75, 373]
    for i in range(size):
        if i == 0:
            continue
        if sectionOfTime[0]<=x[i]<sectionOfTime[1]:
            Ti = tempatres[0]
            res[y[i]] = getKAtOnePoint(y[i], Ti, y[i - 1], diat)
        if sectionOfTime[1]<=x[i]<sectionOfTime[2]:
            # res[y[i]] = getSubsectionTempature(tempatres, None, 1, dx, x[i]*7/6)
            Ti = getSubsectionTempature(tempatres, None, 1, dx, x[i]*7/6)
            K = getKAtOnePoint(y[i], Ti, y[i - 1], diat)
            res[y[i]] = K
        if sectionOfTime[2]<=x[i]<sectionOfTime[3]:
            Ti = tempatres[1]
            res[y[i]] = getKAtOnePoint(y[i], Ti, y[i - 1], diat)
        if sectionOfTime[3]<=x[i]<sectionOfTime[4]:
            # res[y[i]] = getSubsectionTempature(tempatres, None, 2, dx, x[i] * 7 / 6)
            Ti = getSubsectionTempature(tempatres, None, 1, dx, x[i] * 7 / 6)
            K = getKAtOnePoint(y[i], Ti, y[i - 1], diat)
            res[y[i]] = K
        if sectionOfTime[4]<=x[i]<sectionOfTime[5]:
            Ti = tempatres[2]
            res[y[i]] = getKAtOnePoint(y[i], Ti, y[i - 1], diat)
        if sectionOfTime[5]<=x[i]<sectionOfTime[6]:
            # res[y[i]] = getSubsectionTempature(tempatres, None, 3, dx, x[i] * 7 / 6)
            Ti = getSubsectionTempature(tempatres, None, 1, dx, x[i] * 7 / 6)
            K = getKAtOnePoint(y[i], Ti, y[i - 1], diat)
            res[y[i]] = K
        if sectionOfTime[6]<=x[i]<sectionOfTime[7]:
            Ti = tempatres[3]
            res[y[i]] = getKAtOnePoint(y[i], Ti, y[i - 1], diat)
        if sectionOfTime[7]<=x[i]<=sectionOfTime[10]:
            # res[y[i]] = getSubsectionTempature(tempatres, None, 4, dx, x[i] * 7 / 6)
            Ti = getSubsectionTempature(tempatres, None, 1, dx, x[i] * 7 / 6)
            K = getKAtOnePoint(y[i], Ti, y[i - 1], diat)
            res[y[i]] = K
        # if sectionOfTime[8]<=x[i]<=sectionOfTime[10]:  changed for the new alpha , the difference end linespace
        #     Ti = tempatres[4]
        #     res[y[i]] = getKAtOnePoint(y[i], Ti, y[i - 1], diat)

    return res


#得到不同温差下的k(只记录升温阶段)
def getKsTempDiff(x, y, tempatres, section):
    tempatres = [175, 195, 235, 255, 25]
    tempatres2 = [185, 205, 245, 265, 25]
    section = [0, 147.5, 200, 230, 295]
    size = x.shape[0]
    res = {}
    diat = 0.5
    dx = 5
    dxlast = 91
    sectionOfTime = [21.4, 169.3, 173.6, 199.7, 204, 230.14, 234.4, 291, 373.2]
    sectionOfDis = [25, 197.5, 202.5, 233, 238, 268.5, 273.5, 339.5, 435.5]
    tempdiff = []
    ks = []
    maxDiffTemp = -1
    for i in range(size):
        if i == 0:
            continue
        if sectionOfTime[0]<=x[i]<sectionOfTime[1]:
            Ti = tempatres[0]
            K = getKAtOnePoint(y[i], Ti, y[i - 1], diat)
            tempdiff.append(abs(Ti - y[i-1]))
            ks.append(K)
            res[y[i]] = K
        if sectionOfTime[1]<=x[i]<sectionOfTime[2]:
            Ti = getSubsectionTempature(tempatres, None, 1, dx, x[i]*7/6)
            K = getKAtOnePoint(y[i], Ti, y[i - 1], diat)
            tempdiff.append(abs(Ti - y[i]))
            ks.append(K)
            res[y[i]] = K
        if sectionOfTime[2]<=x[i]<sectionOfTime[3]:
            Ti = tempatres[1]
            K = getKAtOnePoint(y[i], Ti, y[i - 1], diat)
            tempdiff.append(abs(Ti - y[i]))
            ks.append(K)
            res[y[i]] = K
        if sectionOfTime[3]<=x[i]<sectionOfTime[4]:
            Ti = getSubsectionTempature(tempatres, None, 2, dx, x[i] * 7 / 6)
            K = getKAtOnePoint(y[i], Ti, y[i - 1], diat)
            tempdiff.append(abs(Ti - y[i]))
            ks.append(K)
            res[y[i]] = K
        if sectionOfTime[4]<=x[i]<sectionOfTime[5]:
            Ti = tempatres[2]
            K = getKAtOnePoint(y[i], Ti, y[i - 1], diat)
            tempdiff.append(abs(Ti - y[i]))
            ks.append(K)
            res[y[i]] = K
        if sectionOfTime[5]<=x[i]<sectionOfTime[6]:
            Ti = getSubsectionTempature(tempatres, None, 3, dx, x[i] * 7 / 6)
            K = getKAtOnePoint(y[i], Ti, y[i - 1], diat)
            tempdiff.append(abs(Ti - y[i]))
            ks.append(K)
            res[y[i]] = K
        if sectionOfTime[6]<=x[i]<sectionOfTime[7]:
            Ti = tempatres[3]
            K = getKAtOnePoint(y[i], Ti, y[i - 1], diat)
            tempdiff.append(abs(Ti - y[i]))
            ks.append(K)
            res[y[i]] = K

        if sectionOfTime[7]<=x[i]<=sectionOfTime[8]:
            Ti = getSubsectionTempature(tempatres, None, 4, dxlast, x[i] * 7 / 6)
            K = getKAtOnePoint(y[i], Ti, y[i - 1], diat)
            tempdiff.append(abs(Ti - y[i]))
            maxDiffTemp = max(maxDiffTemp, abs(Ti - y[i]))
            ks.append(K)
            res[y[i]] = K

        # if sectionOfTime[8]<=x[i]<=sectionOfTime[10]:#改成线性区域
        #     #获取线性区域温度
        #     #getKAtOnepoint...
        #     Ti = getSubsectionTempature(tempatres, None, 5, dx, x[i] * 7 / 6)
        #     K = getKsAtTimePoints(y[i], Ti, y[i-1], diat)
        #     tempdiff.append(abs(Ti - y[i]))
        #     ks.append(K)
    return tempdiff, ks, res


def getKsTempDiffBeforePeek(x, y, tempatres, section):
    tempatres = [175, 195, 235, 255, 25]
    tempatres2 = [185, 205, 245, 265, 25]
    section = [0, 147.5, 200, 230, 295]
    size = x.shape[0]
    res = {}
    diat = 0.5
    dx = 5
    dxlast = 91
    sectionOfTime = [21.4, 169.3, 173.6, 199.7, 204, 230.14, 234.4, 291, 373.2]
    sectionOfDis = [25, 197.5, 202.5, 233, 238, 268.5, 273.5, 339.5, 435.5]
    tempdiff = []
    ks = []
    maxDiffTemp = -1
    for i in range(size):
        if i == 0:
            continue
        if sectionOfTime[0]<=x[i]<sectionOfTime[1]:
            Ti = tempatres[0]
            K = getKAtOnePoint(y[i], Ti, y[i - 1], diat)
            if K < 0 or K > 0:
                tempdiff.append(abs(Ti - y[i]))
                ks.append(K)
                res[abs(Ti - y[i - 1])] = K
    return tempdiff, ks, res


def getKsTempDiffAfterPeek(x, y, tempatres, section):
    tempatres = [175, 195, 235, 255, 25]
    tempatres2 = [185, 205, 245, 265, 25]
    section = [0, 147.5, 200, 230, 295]
    size = x.shape[0]
    res = {}
    diat = 0.5
    dx = 5
    dxlast = 91
    sectionOfTime = [21.4, 169.3, 173.6, 199.7, 204, 230.14, 234.4, 291.002, 373.2]
    sectionOfDis = [25, 197.5, 202.5, 233, 238, 268.5, 273.5, 339.5, 435.5]
    tempdiff = []
    ks = []
    maxDiffTemp = -1
    for i in range(size):
        if i == 0:
            continue
        if sectionOfTime[7] <= x[i] <= sectionOfTime[8]:
            Ti = getSubsectionTempature(tempatres, None, 4, dxlast, x[i] * 7 / 6)
            K = getKAtOnePoint(y[i], Ti, y[i - 1], diat)
            if K<0 or K>0:
                tempdiff.append(abs(Ti - y[i]))
                ks.append(K)
                res[abs(Ti - y[i - 1])] = K
    return tempdiff, ks, res