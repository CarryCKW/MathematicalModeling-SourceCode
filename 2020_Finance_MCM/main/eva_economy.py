import numpy as np
import main.read_file as rf
import main.write_file as wf
import main.eva_tech as et


ic = 0.03
Rt = 1000000


def get_V2():
    Ns = et.getN()
    # print(Ns)
    V2 = []
    for i in range(len(Ns)):
        N = Ns[i]
        num = 0
        for j in range(int(N + 1)):
            if j == 0:
                continue
            else:
                num += Rt / ((1 + ic) ** j)
        V2.append(num)
    V2_max = max(V2)
    # print(V2)
    for k in range(len(V2)):
        V2[k] = V2[k] * 10 / V2_max
    # print(V2)
    return V2


if __name__ == '__main__':
    Vs = get_V2()
    file1 = r"经济价值"
    example_file1 = r"example_经济价值"
    wf.WriteFile(Vs, example_file1)