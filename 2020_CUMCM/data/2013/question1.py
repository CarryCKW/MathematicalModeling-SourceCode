from PIL import Image
import numpy as np
import cv2
import os
import torch
from difflib import SequenceMatcher


# 数组写入文件
def WriteFile(arr):
    filePath = "data/resbinary.txt"
    np.savetxt(filePath, arr, fmt="%d")


# 全局阈值
def threshold_demo(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # ret, binary = cv2.threshold(gray,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_TRIANGLE)
    # ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_TRUNC)
    ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    print("阈值：", ret)
    print("图像数组", binary)
    cv2.imshow("binary", binary)


# 局部阈值
def local_threshold(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    # binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,25,10)
    binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 25, 10)
    cv2.imshow("binary ", binary)


def custom_threshold(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    h, w = gray.shape[:2]
    m = np.reshape(gray, [1, w * h])
    mean = m.sum() / (w * h)
    # binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,25,10)
    ret, binary = cv2.threshold(gray, mean, 255, cv2.THRESH_BINARY)
    WriteFile(binary)
    print("picture_size:", torch.from_numpy(binary).size())
    cv2.imshow("binary ", binary)


def custom_threshold2(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    h, w = gray.shape[:2]
    m = np.reshape(gray, [1, w * h])
    mean = m.sum() / (w * h)
    # binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,25,10)
    ret, binary = cv2.threshold(gray, mean, 255, cv2.THRESH_BINARY)
    return binary


if __name__ == "__main__":
    # img = cv2.imread("data/P1/009.bmp")
    # cv2.namedWindow("input image", cv2.WINDOW_AUTOSIZE)
    # cv2.imshow("input image", img)
    # custom_threshold(img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    numOfPhotos = 19
    row = 1980
    col = 72
    bs = np.ndarray([19, 1980, 72])
    bsOf2col = np.ndarray([19, 1980, 2])
    print(torch.from_numpy(bs).size())
    for i in range(numOfPhotos):
        filePath = "data/P1/0"
        if i < 10:
            filePath += "0"
            filePath += str(i) + ".bmp"
        else:
            filePath += str(i) + ".bmp"
        img = cv2.imread(filePath)
        # b = np.ndarray([1980, 72])
        b = custom_threshold2(img)
        bs[i] = b
        # bsOf2col[i][:][0] = b[:][0]
        # bsOf2col[i][:][1] = b[:][col - 1]
        for t in range(2):
            if t == 0:
                j = 0
                for k in range(row):
                    bsOf2col[i][k][t] = b[k][j]
            else:
                j = col - 1
                for k in range(row):
                    bsOf2col[i][k][t] = b[k][j]

    # print(torch.from_numpy(bsOf2col[0][0]).size())
    # print(bsOf2col[0])
    WriteFile(bsOf2col[0])