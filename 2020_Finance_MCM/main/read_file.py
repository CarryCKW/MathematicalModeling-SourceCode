from io import open
import glob
import numpy as np
import math
import os
import xlrd
from sklearn import preprocessing
import matplotlib.pyplot as plt
import matplotlib as mpl


def excel_to_matrix(path, need1line=False):
    table = xlrd.open_workbook(path).sheets()[0]  # 获取第一个sheet表
    row = table.nrows  # 行数
    if not need1line:
        row -= 1
    col = table.ncols  # 列数
    datamatrix = np.zeros((row, col))  # 生成一个nrows行ncols列，且元素均为0的初始矩阵
    for x in range(col):
        # if x == 0:
        #     continue
        cols = np.array(table.col_values(x))  # 把list转换为矩阵进行矩阵操作
        if not need1line:
            cols = cols[1:]
        datamatrix[:, x] = cols  # 按列把数据存进矩阵中
    return datamatrix


# filepath = r"C:\Users\蔡小蔚\Desktop\data\data1.xlsx"
# res = excel_to_matrix(filepath, False)

# print(res[:, :])

def readFormTxt(filePath):
    a = np.loadtxt(filePath)
    return a
