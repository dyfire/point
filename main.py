# -*- coding: UTF-8 -*-

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt


def analyze(data_frame, col):
    return data_frame.groupby([col])[col].count() \
        .reset_index(name='num').sort_values(by='num', ascending=False)


if __name__ == '__main__':
    pd.set_option('display.max_row', 100,
                  'display.max_column', 1000,
                  'display.max_colwidth', 1000,
                  'display.width', 1000)

    file_data = os.path.abspath('../../Downloads') + '/userprofileAnalyst.csv'
    if not os.path.exists(file_data):
        exit()

    df = pd.read_csv(file_data, encoding='unicode_escape',
                     low_memory=False)

    s = pd.Series(np.random.randn(100).cumsum(), index=np.arange(0, 100))
    s.plot()
    exit()
    # 列名
    # print(df.columns.values)
    # 数据概览
    print(df.info())

    # 总行数
    rows = df.shape[0]
    print(rows)

    # 总列数
    columns = df.shape[1]
    print(columns)

    # 国家
    country_nums = df.groupby(['Country'])['Country'].count() \
        .reset_index(name='num').sort_values(by='num', ascending=False)
    print(country_nums)

    # 国家10
    top_country_num = country_nums.head(10)
    print(top_country_num)

    # 年龄段
    age_period = analyze(df, 'Age')

    # 年龄段百分比
    age_period['rate'] = age_period['num'] / age_period.sum()['num']
    age_period['rate'] = age_period['rate'].map(lambda x: round(x, 4))

    # 年龄段前12
    age_period_top = age_period.head(12)
    age_period_top_sum = age_period_top.sum()

    # 插入'其他'行
    obj = pd.DataFrame({
        'Age': '其他',
        'num': 0,
        'rate': (1 - age_period_top_sum['rate'])
    }, index=[0])

    age_period_top = age_period_top.append(obj, ignore_index=True)
    age_period_top['Age'].value_counts().head(10).plot.bar()
    print(age_period_top)

    # 年龄平均值
    age_mean = age_period.mean()['Age']

    exit()

    # 性别
    gender = df.groupby(['GenderSelect'])['GenderSelect'].count().reset_index(name='num') \
        .sort_values(by='num', ascending=False)
    print(gender)

    # 性别占比
    gender['gender_rate'] = gender['num'] / gender.sum()['num']
    print(gender)

    # 职位
    job = df.groupby(['CurrentJobTitleSelect'])['CurrentJobTitleSelect'].count(). \
        reset_index(name='num').sort_values(by='num', ascending=False)
    print(job)

    # 语言
    lang = df.groupby(['LanguageRecommendationSelect'])['LanguageRecommendationSelect'].count() \
        .reset_index(name='num').sort_values(by='num', ascending=False)
    print(lang)

    # 学习平台
    platform = df.groupby(['LearningPlatformSelect'])['LearningPlatformSelect'].count() \
        .reset_index(name='num').sort_values(by='num', ascending=False)
    print(platform)

    writer = pd.ExcelWriter
