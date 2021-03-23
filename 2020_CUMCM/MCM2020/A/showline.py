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


res = excel_to_matrix(datafile, False)

print(res.shape)

x = res[:, 0]
y = res[:, 1]
print("y Shape:", y.shape[0])


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
    if 240<=peek<=250:
        return True
    else:
        return False


print(checkPeek(y))
