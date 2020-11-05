# -*- coding: UTF-8 -*-

import pandas as pd
import numpy as np
import os
from pyecharts import options as opts
from pyecharts.charts import Pie, Bar
from pyecharts.globals import ThemeType
from pyecharts.charts import Pie, Bar, Line
from pyecharts.faker import Faker
from pyecharts.charts import Page, WordCloud


def analyze(data_frame, col):
    """
    按照指定列分组统计
    :param data_frame: DataFrame
    :param col: 列名
    :return: DataFrame
    """
    df = data_frame.groupby([col])[col].count() \
        .reset_index(name='num').sort_values(by='num', ascending=False)
    total = df['num'].sum()
    df['percent'] = round(df['num'] / total, 2)

    return df


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

    big_data_importance(df)

    print("finished")


def excel_writer(df):
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
    bar.add_yaxis("年龄分布图", data_y)
    bar.render('bar.html')


def chart_employment_status(df):
    data = analyze(df, 'EmploymentStatus')
    data_pair_pie = [list(z) for z in zip(data['EmploymentStatus'],
                                          [int(x) for x in data['num']])]

    c = (Pie(init_opts=opts.InitOpts(theme=ThemeType.MACARONS, width='1500px'))
         .set_global_opts(title_opts=opts.TitleOpts(title="就业情况"),
                          legend_opts=opts.LegendOpts(
                              orient="vertical",
                              pos_top="15%",
                              pos_left="2%"),
                          )
         .add(data_pair=data_pair_pie, series_name='就业情况', radius=["40%", "75%"], )
         )
    c.render('pie_status.html')


def chart_plan(df):
    data_tool = analyze(df, 'MLToolNextYearSelect').head(20)

    data_tool_x = [y for y in data_tool['MLToolNextYearSelect']]
    data_tool_y = [int(y) for y in data_tool['num']]

    c = (Bar(init_opts=opts.InitOpts(width='1000px')).set_global_opts()
         .add_xaxis(data_tool_x)
         .add_yaxis("工具", data_tool_y)
         .set_global_opts(title_opts=opts.TitleOpts(title="明年使用工具"),
                          xaxis_opts=opts.AxisOpts(name_rotate=60, axislabel_opts={"rotate": 45}))
         )
    c.render('bar_plan.html')


def chart_lang(df):
    data_python = analyze(df, 'JobSkillImportancePython')
    data_r = analyze(df, 'JobSkillImportanceR')
    data_sql = analyze(df, 'JobSkillImportanceSQL')

    x = [y for y in data_python['JobSkillImportancePython']]
    data_python_y = [int(y) for y in data_python['num']]
    data_r_y = [int(y) for y in data_r['num']]
    data_sql_y = [int(y) for y in data_sql['num']]

    c = (
        Bar(init_opts=opts.InitOpts(width='1000px'))
            .add_xaxis(x)
            .add_yaxis('Python', data_python_y)
            .add_yaxis('R', data_r_y)
            .add_yaxis('SQL', data_sql_y)
            .set_series_opts(label_opts=opts.LabelOpts(position='right'
                                                       # 设置数据标签所在的位置'top'，'left'，'right'，'bottom'，'inside'，'insideLeft'，'insideRight'
                                                       # 'insideTop'，'insideBottom'， 'insideTopLeft'，'insideBottomLeft'
                                                       # 'insideTopRight'，'insideBottomRight'
                                                       , font_size=12
                                                       # ,formatter #数据标签显示格式
                                                       )  ##设置数据标签的格式s
                             )
            .reversal_axis()
    )
    c.render('line_lang.html')


def pie_map(df):
    data = analyze(df, 'Country').head(20)
    data_x = [y for y in data['Country']]
    data_y = [int(y) for y in data['num']]
    data_per = data['percent'] * 100
    c = (Bar(init_opts=opts.InitOpts(width="1200px", height="500px"))
        .add_xaxis(xaxis_data=data_x)
        .add_yaxis(series_name='国家', yaxis_data=data_y,
                   label_opts=opts.LabelOpts(is_show=False),
                   )
        .extend_axis(
        yaxis=opts.AxisOpts(
            name="百分比", type_="value", min_=0,
            axislabel_opts=opts.LabelOpts(formatter="{value} %"),
            position='top'
        ))
        .set_global_opts(
        tooltip_opts=opts.TooltipOpts(
            is_show=True, trigger="axis", axis_pointer_type="cross"
        ),
        xaxis_opts=opts.AxisOpts(
            type_="category",
            axispointer_opts=opts.AxisPointerOpts(is_show=True, type_="shadow"),
            axislabel_opts={"rotate": 45}, name_rotate=45
        ),
        yaxis_opts=opts.AxisOpts(
            # name="水量", type_="value",
            # min_=0, max_=250, interval=50,
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
            name_rotate=45, axislabel_opts={"rotate": 45}
        ),
        title_opts=opts.TitleOpts(title="从业者所属国家"),
    )
    )

    line = (
        Line()
            .add_xaxis(xaxis_data=data_x)
            .add_yaxis(
            z_level=10,
            series_name="占比",
            yaxis_index=1,
            y_axis=data_per,
            label_opts=opts.LabelOpts(is_show=False, formatter="{value} %"),
        )

    )
    c.overlap(line).render('country.html')


def program_lang(df):
    data = analyze(df, 'LanguageRecommendationSelect').head(10)
    data_x = [y for y in data['LanguageRecommendationSelect']]
    data_y = [int(y) for y in data['num']]
    data_per = data['percent'] * 100
    c = (Bar(init_opts=opts.InitOpts(width="1200px", height="500px"))
        .add_xaxis(xaxis_data=data_x)
        .add_yaxis(series_name='编程语言', yaxis_data=data_y,
                   label_opts=opts.LabelOpts(is_show=False),
                   )
        .extend_axis(
        yaxis=opts.AxisOpts(
            name="百分比", type_="value", min_=0,
            axislabel_opts=opts.LabelOpts(formatter="{value} %"),
            position='top'
        ))
        .set_global_opts(
        tooltip_opts=opts.TooltipOpts(
            is_show=True, trigger="axis", axis_pointer_type="cross"
        ),
        xaxis_opts=opts.AxisOpts(
            type_="category",
            axispointer_opts=opts.AxisPointerOpts(is_show=True, type_="shadow"),
            axislabel_opts={"rotate": 45}, name_rotate=45
        ),
        yaxis_opts=opts.AxisOpts(
            # name="水量", type_="value",
            # min_=0, max_=250, interval=50,
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
            name_rotate=45, axislabel_opts={"rotate": 45}
        ),
        title_opts=opts.TitleOpts(title="编程语言"),
    )
    )

    line = (
        Line()
            .add_xaxis(xaxis_data=data_x)
            .add_yaxis(
            z_level=10,
            series_name="占比",
            yaxis_index=1,
            y_axis=data_per,
            label_opts=opts.LabelOpts(is_show=False, formatter="{value} %"),
        )

    )
    c.overlap(line).render('program.html')


def program_cloud_lang(df):
    data = analyze(df, 'LanguageRecommendationSelect')
    words = [list(z) for z in zip(data['LanguageRecommendationSelect'],
                                  [int(x) for x in data['num']])]
    c = (
        WordCloud()
            .add("", words, word_size_range=[20, 150], shape='cardioid')
            .set_global_opts(title_opts=opts.TitleOpts(title="推荐编程语言"))
    )
    c.render('program_lang_cloud.html')


def big_data_importance(df):
    data_python = analyze(df, 'JobSkillImportanceBigData')
    data_r = analyze(df, 'JobSkillImportanceDegree')
    data_sql = analyze(df, 'JobSkillImportanceEnterpriseTools')
    print(data_python)
    print(data_r)

    data =
    return
    x = [y for y in data_python['JobSkillImportanceBigData']]
    data_python_y = [int(y) for y in data_python['num']]
    data_r_y = [int(y) for y in data_r['num']]
    data_sql_y = [int(y) for y in data_sql['num']]
    
    c = (
        Bar(init_opts=opts.InitOpts(width='1000px'))
            .add_xaxis(x)
            .add_yaxis('Python', data_python_y)
            .add_yaxis('R', data_r_y)
            .add_yaxis('SQL', data_sql_y)
            .set_series_opts(label_opts=opts.LabelOpts(position='right'
                                                       # 设置数据标签所在的位置'top'，'left'，'right'，'bottom'，'inside'，'insideLeft'，'insideRight'
                                                       # 'insideTop'，'insideBottom'， 'insideTopLeft'，'insideBottomLeft'
                                                       # 'insideTopRight'，'insideBottomRight'
                                                       , font_size=12
                                                       # ,formatter #数据标签显示格式
                                                       )  ##设置数据标签的格式s
                             )
            .reversal_axis()
    )
    c.render('line_importance.html')


if __name__ == '__main__':
    run()
