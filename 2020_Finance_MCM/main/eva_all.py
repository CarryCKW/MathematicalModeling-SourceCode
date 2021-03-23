import numpy as np
import main.read_file as rf
import main.write_file as wf
import main.eva_shichang as sc
import main.eva_tech as te
import main.eva_3_4 as e34
import main.eva_economy as econ


def get_all_matric():
    file1 = "all.txt"
    file2 = "all2.txt"
    all = []
    temp = np.zeros((26, 5))
    us, vs, v_all = sc.eva_V()
    P = te.getP()
    w1 = [0.61961722, 0.15603402, 0.22434875]
    w2 = [0.17169432, 0.44142785, 0.38687783]
    ans3, ans4 = e34.get_socre(w1, w2)
    Vs = econ.get_V2()
    all.append(v_all)
    all.append(P)
    all.append(ans3)
    all.append(ans4)
    all.append(Vs)

    temp[:, 0] = v_all
    temp[:, 1] = P
    temp[:, 2] = ans3
    temp[:, 3] = ans4
    temp[:, 4] = Vs
    return temp



if __name__ == '__main__':
    file1 = "all.txt"
    file2 = "all2.txt"
    all = []
    temp = np.zeros((26, 5))
    us, vs, v_all = sc.eva_V()
    P = te.getP()
    w1 = [0.61961722, 0.15603402, 0.22434875]
    w2 = [0.17169432, 0.44142785, 0.38687783]
    ans3, ans4 = e34.get_socre(w1, w2)
    Vs = econ.get_V2()
    all.append(v_all)
    all.append(P)
    all.append(ans3)
    all.append(ans4)
    all.append(Vs)

    temp[:, 0] = v_all
    temp[:, 1] = P
    temp[:, 2] = ans3
    temp[:, 3] = ans4
    temp[:, 4] = Vs
    print(temp)

    wf.WriteFile(temp, file2)
    print("all", len(all[3]))