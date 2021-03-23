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
import fun_read


path = 'data/2017/附件一已结束项目任务数据.xls'
need1stline = False
res = fun_read.excel_to_matrix(path, need1stline)
x = res[:, 1]
y = res[:, 2]
z = res[:, 3]
flag = res[:, 4]

size = res.shape[0]
print(size)

fig = plt.figure()