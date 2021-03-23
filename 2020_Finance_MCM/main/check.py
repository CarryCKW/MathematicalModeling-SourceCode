import numpy as np
import main.read_file as rf
import main.write_file as wf
import main.eva_all as ea
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from scipy.stats import chi2 # 卡方分布


"""
origin  a 6
        b 1.4
        c 0.5
"""
def get_socre(x, a, b ,c):
    return a / (b + np.exp(-c * (x - 12)))


def check(a, b, c):
    matric = rf.readFormTxt(r"26个案例五个维度最终得分.txt")
    x = matric[:]
    yeva = get_socre(x, a, b, c)
    yeva = yeva * 10000000
    yreal = rf.readFormTxt(r"26交易价格.txt")
    yreal = yreal[:]
    wcls = []
    evgsc = 0
    for i in range(len(yeva)):
        num = abs(yeva[i] - yreal[i])
        # print(num)
        num = num / yreal[i]
        wcls.append(num)
        evgsc += num
    evgsc = evgsc / len(yeva)
    return evgsc




if __name__ == '__main__':
    font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=17)
    a = np.linspace(5, 7, 100)
    b = np.linspace(1, 2, 100)
    c = np.linspace(0, 1, 100)
    # b = 1.4
    # c =0.5
    evgs = []
    minnum = 1000
    gooda = 7
    goodb = 1.73469
    goodc = 0.55556
    # for i in range(len(a)):
    #     num = check(a[i], 1.4, 0.5)
    #     evgs.append(num)
    #     if minnum > num:
    #         minnum = num
    #         gooda = a[i]

    minnum = 10000
    for i in range(len(c)):
        num = check(7, 1.73469, c[i])
        evgs.append(num)
        if minnum > num:
            minnum = num
            goodb = c[i]
    # print(evgs)
    # print(gooda)
    # print(len(c))

    # for i in range(len(a)):
    #     for j in range(len(b)):
    #         for k in range(len(c)):
    #             num = check(a[i], b[j], c[k])
    #             evgs.append(num)
    #             if minnum > num:
    #                 minnum = num
    #                 gooda = a[i]
    #                 goodb = b[j]
    #                 goodc = c[k]
    #
    # print(gooda)
    # print(goodb)
    # print(goodc)

    plt.plot(c, evgs, linewidth = 2)
    plt.xlabel(u"值 c ", fontproperties=font_set)
    plt.ylabel(u"整体误差率", fontproperties=font_set)
    plt.show()