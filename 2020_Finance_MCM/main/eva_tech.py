import numpy as np
import main.read_file as rf
import main.write_file as wf


def get_matric():
    res = rf.excel_to_matrix(example_filepath, False)
    return res


def getPmin():
    matric = get_matric()
    print(matric.shape)
    Pmins = []
    for i in range(matric.shape[0]):
        num = 0
        for j in range(matric.shape[1]):
            if j == 0:
                continue
            else:
                num += matric[i][j]
        Pmins.append(num)
    return Pmins


def getN():
    matric = get_matric()
    Ns = []
    for i in range(matric.shape[0]):
        Ns.append(matric[i][0])
    return Ns


Mt = 1000000
ic = 0.05
Pt = 100000
def getAB(N, fir_or_second):
    if fir_or_second == "fir":
        num = 0
        for i in range(int(N + 1)):
            if i == 0:
                continue
            num += Mt / ((1 + ic) ** i)
        return num
    elif fir_or_second == "sec":
        num = 0
        for i in range(int(N + 1)):
            if i == 0:
                continue
            num += Pt / ((1 + ic) ** i)
        return num


def getPmax():
    Pmax = []
    Ns = getN()
    for i in range(len(Ns)):
        fir = getAB(Ns[i], "fir")
        sec = getAB(Ns[i], "sec")
        Pmax.append(fir - sec)

    return Pmax


def getP():
    Pmin = getPmin()
    Pmax = getPmax()
    Pmax_max = max(Pmax)
    print("maxmax:" , Pmax_max)
    assert len(Pmin) == len(Pmax)
    P = []
    for i in range(len(Pmin)):
        num = 0.618 * Pmin[i] + 0.382 * Pmax[i]
        num = num * 10 / Pmax_max
        P.append(num)
    return P



if __name__ == '__main__':
    P = getP()
    file1 = r"技术价值"
    example_file1 = r"example_技术价值"
    wf.WriteFile(P, example_file1)
    # print(P)