import numpy as np
import main.read_file as rf
import main.write_file as wf


def get_y_qqkpd(num, x_min, x_max):
    y = 5 + 5 * (num - x_min) / (x_max - x_min)
    return y


def get_y_syyxq(num):
    return num/2


def get_socre(w1, w2):
    res = rf.excel_to_matrix(example_filepath, False)
    # print(res)
    rows = res.shape[0]
    cols = res.shape[1]
    w = [0, w1[0], w1[1], w1[2], w2[0], w2[1], w2[2]]
    print(rows, cols)
    ans1 = []
    ans2 = []
    max_x = -1
    min_x = 10000
    for i in range(rows):
        for j in range(cols):
            if j == 1:
                max_x = max(max_x, res[i][j])
                min_x = min(min_x, res[i][j])
    print(max_x, min_x)

    for i in range(rows):
        num1 = 0
        num2 = 0
        for j in range(cols):
            if j == 0:
                num1 += 0
            elif j == 1:
                num1 += get_y_qqkpd(res[i][j], min_x, max_x) * w[j]
            elif j == 2:
                num1 += get_y_syyxq(res[i][j]) * w[j]
            elif j == 3:
                num1 += res[i][j] * w[j]
            elif j == 4:
                num2 += res[i][j] * w[j]
            elif j == 5:
                num2 += res[i][j] * 10 * w[j]
            elif j == 6:
                num2 += res[i][j] * 10 * w[j]
        ans1.append(num1)
        ans2.append(num2)
        num1 = 0
        num2 = 0
    return ans1, ans2


if __name__ == '__main__':
    w1 = [0.61961722, 0.15603402, 0.22434875]
    w2 = [0.17169432, 0.44142785, 0.38687783]

    ans3, ans4 = get_socre(w1, w2)
    print((ans3))
    print((ans4))
    file1 = r"法律价值"
    example_file1 = r"example_法律价值"
    file2 = r"战略价值"
    example_file2 = r"example_战略价值"
    wf.WriteFile(ans3, example_file1)
    wf.WriteFile(ans4, example_file2)
