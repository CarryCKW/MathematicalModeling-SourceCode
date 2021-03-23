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


def WriteFile(arr, filePath):
    np.savetxt(filePath, arr, fmt="%.2f")