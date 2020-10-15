# -*- coding: UTF-8 -*-

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import xlsxwriter


def analyze(data_frame, col):
    return data_frame.groupby([col])[col].count() \
        .reset_index(name='num').sort_values(by='num', ascending=False)


def multi(data_frame, col):
    data = {}
    for c in col:
        new_index = c + '_num'
        data[c] = data_frame.groupby([c])[c].count() \
            .reset_index(name=new_index).sort_values(by=new_index, ascending=False)

    return data


def run():
    pd.set_option('display.max_row', 100,
                  'display.max_column', 1000,
                  'display.max_colwidth', 1000,
                  'display.width', 1000)

    file_data = os.path.abspath('../../Downloads') + '/userprofileAnalyst.csv'
    if not os.path.exists(file_data):
        exit(0)

    df = pd.read_csv(file_data, encoding='unicode_escape',
                     low_memory=False)

    cols = [
        'Country',
        'Age',
        'EmploymentStatus',
        'MLToolNextYearSelect',
        'MLMethodNextYearSelect',
        'LanguageRecommendationSelect',
        'JobSkillImportanceBigData',
        'JobSkillImportanceDegree',
        'JobSkillImportanceEnterpriseTools',
        'JobSkillImportancePython',
        'JobSkillImportanceR',
        'JobSkillImportanceSQL']

    dt = multi(df, cols)
    output_file = 'output.xlsx'
    writer = pd.ExcelWriter(output_file)
    i = 1
    for (k, v) in dt.items():
        v.to_excel(writer, sheet_name='Sheet' + str(i), index=False)
        i += 1
    writer.save()
    writer.close()
    return

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

    # 性别
    gender = df.groupby(['GenderSelect'])['GenderSelect'].count().reset_index(name='num') \
        .sort_values(by='num', ascending=False)
    print(gender)

    # 性别占比
    gender['gender_rate'] = gender['num'] / gender.sum()['num']
    print(gender)

    # 当前职称
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

    # 工作中使用SQL的频率
    sql_frequent = analyze(df, 'WorkToolsFrequencySQL')
    print(sql_frequent)

    # SQL重要性
    sql_important = analyze(df, 'JobSkillImportanceSQL')
    print(sql_important)

    # 在线学习课时
    study_time = analyze(df, 'LearningCategoryOnlineCourses')
    print(study_time)

    # 就业情况
    employment_status = analyze(df, 'EmploymentStatus')


if __name__ == '__main__':
    run()
