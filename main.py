# -*- coding: UTF-8 -*-

import pandas as pd
import numpy as np
import os
from pyecharts import options as opts
from pyecharts.charts import Pie, Bar
from pyecharts.globals import ThemeType


def analyze(data_frame, col):
    """
    按照指定列分组统计
    :param data_frame: DataFrame
    :param col: 列名
    :return: DataFrame
    """
    return data_frame.groupby([col])[col].count() \
        .reset_index(name='num').sort_values(by='num', ascending=False)


def multi(data_frame, col):
    """
    指定多列分别分组统计
    :param data_frame: DataFrame
    :param col: 多列名list
    :return: dict
    """
    data = {}
    for c in col:
        new_index = 'num'
        data[c] = data_frame.groupby([c])[c].count() \
            .reset_index(name=new_index).sort_values(by=new_index, ascending=False)

    return data


def mixed_and_percent(data_frame, col, top=10, is_rate=True):
    """
    获取指定列的处理数据
    :param is_rate:
    :param data_frame: DataFrame
    :param col:
    :param top:
    :return: DataFrame
    """
    row = analyze(data_frame, col)

    if is_rate:
        row['rate'] = row['num'] / row.sum()['num']
        row['rate'] = row['rate'].map(lambda x: round(x, 4))

        # top
        row_top = row.head(top)
        row_top_sum = row_top.sum()

        # 插入'其他'行
        if row.shape[0] > top:
            obj = {}
            for k in row_top.columns.values:
                obj[k] = 'other'
            obj['rate'] = 1 - row_top_sum['rate']
            obj = pd.DataFrame(obj, index=[0])

            row = row_top.append(obj, ignore_index=True)

    return row


def rename(name):
    """
    设置sheet名称
    :param name: string
    :return: string
    """
    if len(name) > 31:
        return name[18:]
    return name


def run():
    """
    运行主程序
    :return:
    """
    pd.set_option('display.max_row', 100,
                  'display.max_column', 1000,
                  'display.max_colwidth', 1000,
                  'display.width', 1000)

    file_data = os.path.abspath('../../Downloads') + '/userprofileAnalyst.csv'
    if not os.path.exists(file_data):
        exit(0)

    df = pd.read_csv(file_data, encoding='unicode_escape',
                     low_memory=False)
    if df.empty:
        print('empty DataFrame')
        exit(0)

    df = df.dropna(subset=['Age'])
    df['Age'] = df['Age'].astype("int")

    df['Country'] = df['Country'].mask(df['Country'] == 'Taiwan', "People 's Republic of China")
    df['Country'] = df['Country'].mask(df['Country'] == 'Hong Kong', "People 's Republic of China")
    df['Country'] = df['Country'].mask(df['Country'] == 'Republic of China', "People 's Republic of China")

    df = df[(df['Age'] <= 60) & (df['Age'] >= 15)]

    chart_gender(df)
    chart_age(df)
    return
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
        'JobSkillImportanceSQL',
        'WorkToolsFrequencySQL',
        'JobSkillImportanceSQL',
        'LearningCategoryOnlineCourses'
    ]

    dt = multi(df, cols)
    output_file = 'output.xlsx'
    writer = pd.ExcelWriter(output_file)

    for (k, v) in dt.items():
        v.to_excel(writer, sheet_name=rename(k), index=False)

    for r in ['Age', 'Country', 'GenderSelect']:
        v = mixed_and_percent(df, r)
        v.to_excel(writer, sheet_name=r + '-mixed', index=False)
    writer.save()
    writer.close()
    print("finished")


def chart_gender(df):
    """
    性别饼图
    :param df: DataFrame
    :return:
    """
    pie_data = analyze(df, 'GenderSelect')
    data_pair_pie = [list(z) for z in zip(pie_data['GenderSelect'],
                                          [int(x) for x in pie_data['num']])]

    c = (Pie()
         .set_global_opts(opts.ToolboxOpts(is_show=True))
         .add(data_pair=data_pair_pie, series_name='性别')
         )
    c.render('pie.html')
    return


def chart_age(df):
    data = analyze(df, 'Age').sort_values(by='Age', ascending=True)
    bar = Bar(init_opts=opts.InitOpts(width='1500px')).set_global_opts()

    data_x = [int(x) for x in data['Age']]
    data_y = [int(x) for x in data['num']]
    bar.add_xaxis(data_x)
    bar.add_yaxis("num", data_y)
    bar.render('bar.html')


if __name__ == '__main__':
    run()
