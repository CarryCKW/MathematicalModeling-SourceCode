import numpy as np
import main.read_file as rf
import main.write_file as wf
import main.eva_all as ea
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from scipy.stats import chi2 # 卡方分布


def eva_socre_all(weight):
    matric = ea.get_all_matric()
    print(matric.shape)
    examples_score = []
    for i in range(matric.shape[0]):
        num = 0
        for j in range(matric.shape[1]):
            num += matric[i][j] * weight[j]
        examples_score.append(num)
    return examples_score


def getMoneyFunc(x):
    y = 6 / (1.4 + np.exp(-0.5*(x - 12)))
    return y


if __name__ == '__main__':
    # weight = [0.5055, 0.2298, 0.3743, 0.3954, 0.6286]
    # examples_score = eva_socre_all(weight)
    # file1 = r"26个案例五个维度最终得分.txt"
    # # wf.WriteFile(examples_score, file1)
    # print(examples_score)

    font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=17)

    matric = rf.readFormTxt(r"26个案例五个维度最终得分.txt")
    x = matric[:]
    # y = getMoneyFunc(x)
    # fileMoney = r"26个案例专利定价.txt"
    # # wf.WriteFile(y*10000000, fileMoney)
    # # print(getMoneyFunc(11.655))
    # m2 = rf.readFormTxt(r"26交易价格.txt")
    # yreal = m2[:]
    # x2 = np.linspace(10, 17, 50)
    # y2 = getMoneyFunc(x2)
    # print(y2)
    # plt.legend()
    # plt.scatter(x, y, label="我们方案计算")
    # plt.scatter(x, yreal/10000000, label="真实交易价格")
    # plt.plot(x2, y2, linewidth=2, c="green", label="映射函数")
    # plt.xlabel(u"五个维度综合得分", fontproperties=font_set)
    # plt.ylabel(u"专利定价(单位:千万)", fontproperties=font_set)
    # plt.legend(prop={'family':'SimHei','size':10})
    # plt.show()
    fileWucha = r"误差率.txt"
    m3 = rf.readFormTxt(fileWucha)
    wc = m3[:]
    plt.scatter(x, wc, label="误差率随得分波动")
    plt.xlabel(u"五个维度综合得分", fontproperties=font_set)
    plt.ylabel(u"误差率", fontproperties=font_set)
    plt.ylim(-0.5, 1)
    plt.show()





