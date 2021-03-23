import numpy as np

RI_dict = {1: 0, 2: 0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45}


def eva_w(array):
    row = array.shape[0]  # 计算出阶数
    a_axis_0_sum = array.sum(axis=0)
    #print(a_axis_0_sum)
    b = array / a_axis_0_sum  # 新的矩阵b
    # print(b)
    b_axis_0_sum = b.sum(axis=0)
    b_axis_1_sum = b.sum(axis=1)  # 每一行的特征向量
    # print(b_axis_1_sum)
    w = b_axis_1_sum / row  # 归一化处理(特征向量)
    nw = w * row
    AW = (w * array).sum(axis=1)
    # print(AW)
    # lamda
    max_max = sum(AW / (row * w))
    # print(max_max)
    # check lamda
    CI = (max_max - row) / (row - 1)
    CR = CI / RI_dict[row]
    if CR < 0.1:
        # print(round(CR, 3))
        # print('满足一致性')
        # print(np.max(w))
        # print(sorted(w,reverse=True))
        # print(max_max)
        # print('特征向量:%s' % w)
        return w
    else:
        print(round(CR, 3))
        print('不满足一致性，请进行修改')


def get_w(array):
    if type(array) is np.ndarray:
        return eva_w(array)
    else:
        print('请输入numpy对象')


# 政策扶持力   市场竞争力   行业影响力
# label
if __name__ == '__main__':

    # 战略价值的成对比矩阵
    a = np.array([
        [1, 1/2, 1/3],
        [2, 1, 3/2],
        [3, 2/3, 1]
    ])

    # 法律价值的成对比矩阵
    b = np.array([
        [1, 3, 4],
        [1/3, 1, 1/2],
        [1/4, 2, 1]
    ])

    res1 = get_w(a)
    res2 = get_w(b)
    print("战略价值权重向量: ", res1)
    print("法律价值权重向量: ", res2)
