import MCM2020.A.mcmutil as mu
import MCM2020.A.evaK as ek
import numpy as np
import MCM2020.A.evaK2 as ek2


#检验斜率
def checkSolpe():
    beforetempdiff, beforeks, beforeres = ek2.getKsBeforePeek()
    aftertempdiff, afterks, afterres = ek2.getKsAfterPeek()
    isOk = True
    for i, it in enumerate(beforetempdiff):
        if it*beforeks[i]<-3 or it*beforeks[i]>3:
            print("before is not ok")
            print(it, beforeks[i])
            isOk = False
            break
    for i, it in enumerate(aftertempdiff):
        if it*afterks[i] < -3 or it*afterks[i]>3:
            print("after is not ok")
            print(it, afterks[i])
            isOk = False
            break
    if isOk:
        print("pass")





if __name__ == '__main__':
    checkSolpe()