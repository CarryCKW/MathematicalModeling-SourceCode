import main.read_file as rf
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties


if __name__ == '__main__':
    m1 = rf.readFormTxt(r"26个案例五个维度最终得分.txt")
    x = m1[:]
    m2 = rf.readFormTxt(r"26个案例专利定价.txt")
    y = m2[:]
    print(x)
    print(y)