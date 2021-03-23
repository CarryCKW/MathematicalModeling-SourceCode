import numpy as np
import main.read_file as rf
import main.write_file as wf
import main.eva_all as ea


if __name__ == '__main__':
    weight = [0.5055, 0.2298, 0.3743, 0.3954, 0.6286]

    res = 0
    for i in range(len(weight)):
        res += weight[i] * example[i]
    print(res)