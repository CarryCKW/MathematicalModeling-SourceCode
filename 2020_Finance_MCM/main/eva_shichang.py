import numpy as np
import main.read_file as rf
import main.write_file as wf


"""

    
"""
def get_matric():
    res = rf.excel_to_matrix(example_filepath, False)
    return res


def get_u(sz, sf):
    return 1 + 2 * (sz * sf) / 3


def get_d(sz, sf):
    return 1 + 1 * (sz + sf) / 3


r = 0.2
delta_t = 2
V_u = 10000000
V_d = 1000000


def get_p(u, d):
    p = (np.exp(-r * delta_t) - d) / (u - d)
    assert p >= 0
    return p


def get_V1(p, V_u, V_d):
    return np.exp(-r * delta_t) * (p * V_u + (1 - p) * V_d)


def get_V_all(vs):
    ans = []
    v_max = -1
    for i in range(len(vs)):
        v_max = max(v_max, vs[i])

    for i in range(len(vs)):
        num = vs[i] * 10 / v_max
        ans.append(num)

    return ans


def eva_V():
    matric = get_matric()
    print(matric.shape)
    us = []
    ds = []
    Vs = []
    for i in range(matric.shape[0]):
        sz = matric[i][0]
        sf = matric[i][1]
        u = get_u(sz, sf)
        d = get_d(sz, sf)
        us.append(u)
        ds.append(d)
        p = get_p(u, d)
        V1 = get_V1(p, V_u, V_d)
        Vs.append(V1)
    v_all = get_V_all(Vs)
    return us, ds, v_all



if __name__ == '__main__':
    us, vs, v_all = eva_V()
    print(us)
    print(vs)
    print(v_all)
    file1 = r"上涨倍数(u)"
    file2 = r"下降倍数(d)"
    file3 = r"市场价值"
    example_file1 = r"example_上涨倍数(u)"
    example_file2 = r"example_下降倍数(d)"
    example_file3 = r"example_市场价值"
    wf.WriteFile(us, example_file1)
    wf.WriteFile(vs, example_file2)
    wf.WriteFile(v_all, example_file3)