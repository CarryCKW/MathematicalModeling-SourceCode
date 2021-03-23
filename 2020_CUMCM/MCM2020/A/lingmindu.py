import MCM2020.A.mcmutil as mu
import MCM2020.A.evaK as ek
import numpy as np
import MCM2020.A.evaK2 as ek2
import math
import random
import MCM2020.A.p2 as p2
import matplotlib.pyplot as plt


def dochange(tempreatures, carv):
    changes = np.linspace(-0.003, 0.003, 5)
    x, y = evaP1(tempreatures, carv, 0)
    plt.plot(x, y, label='origin')
    for i in range(5):
        change = changes[i]
        if change ==0:
            continue
        x, y = evaP1(tempreatures, carv, change)
        plt.plot(x, y, label="k change " + str(change))

    plt.xlabel("Time ( s )")
    plt.ylabel("Temperautre ( °C )")
    plt.legend()
    plt.show()



def evaP1(tempreatures, carv ,change):
    beforetempdiff, beforeks, beforeres = ek2.getKsBeforePeek()
    aftertempdiff, afterks, afterres = ek2.getKsAfterPeek()
    for i, it in enumerate(beforeks):
        beforeks[i] += change
    for i, it in enumerate(afterks):
        afterks[i] += change
    # print(beforeks)
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
        Ti = tempreatures[idx - 1]
        Tn, k = ek2.tfunc(Ti, Tn_1, dalt, beforetempdiff, beforeks)
        x.append(dalt * step)
        y.append(Tn)
        step += 1
        Tn_1 = Tn
    temp = []
    Xplace = 0.5*step*carv
    while Xplace <= allLen:
        Ti = 257 + (25 - 257)/91 * (Xplace - 339.5)
        Tn , k = ek2.tfunc(Ti, Tn_1, dalt, aftertempdiff, afterks)
        x.append(dalt * step)
        y.append(Tn)
        if 340 <=Xplace <=384:
            temp.append(k)
        step += 1
        Tn_1 = Tn
        Xplace = 0.5*step*carv

    return x, y



if __name__ == '__main__':
    tempreatures = [173, 198, 230, 257, 25]
    carv = 1.3
    dochange(tempreatures, carv)
