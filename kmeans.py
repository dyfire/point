from numpy import *
import numpy as np
import pandas as pd


def init_center(df, k):
    """
    https://blog.csdn.net/zouxy09/article/details/17589329
    初始化k个点
    :param df: pandas数据集
    :param k: 需要k个点
    :return:
    """

    x, y = df.shape
    center_point = zeros(k, y)

    for i in range(x):
        pass


def run():
    zeros()
    pass


if __name__ == '__main__':
    df = pd.DataFrame({
        "A": 1,
        "B": np.array([3] * 4, dtype='int32'),
        "C": 6
    })

    center = zeros((3, 3))
    k = 10
    row, col = df.shape
    for i in range(k):
        index = int(random.uniform(0, row))
        print(center[i, :])
        print(df)

    print(center)
