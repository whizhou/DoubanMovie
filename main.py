# 将 solve_data.py 合并，进行数据处理，数据分析和可视化

import pandas as pd
from datetime import datetime
from matplotlib import pyplot as plt
import matplotlib.font_manager as fm

import solve_data

# 设置中文字体
font_path = 'SimHei.ttf'  # 替换为实际字体文件的路径
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.sans-serif'] = [font_prop.get_name()]
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


# 制片地区分布
def region_analyze(data: pd.DataFrame) -> None:
    """
    直接输出各地区数量;饼状图对比各地区占比;柱状图输出前十
    :param data:
    :return: None
    """
    print("Region Analyzing...")

    # 预览 data['regions'] 数据格式
    print(data['regions'])

    # 进行数据拆分和分组
    regions_list = []
    for regions in data['regions']:
        regions_list.extend(regions)
    regions_df = pd.DataFrame(regions_list, columns=['region'])
    # 按 region 列分组
    region_group = regions_df.groupby('region')
    # print(type(regions_df))

    # 查看各地区电影数量
    print(region_group.size())

    """
    绘制比例饼图:
    1.计算每个地区的比例
    2.将占比小于一定阈值的地区合并为“其它”
    3.按比例顺序排序数据
    4.绘制饼图
    """
    # 按各地区影片数降序排序
    region_count = region_group.size().sort_values(ascending=False)

    # 计算每个类别比例
    total = region_count.sum()
    region_percent = (region_count / total) * 100

    # 将占比小于阈值的数据合并为“其它”
    threshold = 2.5  # 设定阈值为 5%
    region_percent_filtered = region_percent[region_percent >= threshold]
    other_percent = region_percent[region_percent < threshold].sum()
    region_percent_filtered['其它地区'] = other_percent

    # 按比例排序
    region_percent_filtered = region_percent_filtered.sort_values(ascending=False)

    # # 绘制饼图
    plt.figure()
    region_percent_filtered.plot.pie(autopct='%1.1f%%', label='', startangle=90, counterclock=False)
    plt.title('Movie Type Proportional Distribution Map')
    plt.show()

    """
    绘制 Pareto Chart
    """
    # 获取影片数量前十的地区
    top_regions = region_count.head(10)

    # 计算累计百分比
    region_percent_sorted = region_percent.sort_values(ascending=False)
    cumulative_percent = region_percent_sorted.cumsum().head(10)

    # 绘制帕累托图
    fig, ax1 = plt.subplots()

    # 条形图
    bars = ax1.bar(top_regions.index, top_regions, color='C0')
    ax1.set_ylabel('影片数量', color='C0', fontproperties=font_prop)
    ax1.tick_params(axis='y', labelcolor='C0')

    # 显示累计百分比的次坐标轴
    ax2 = ax1.twinx()
    ax2.plot(top_regions.index, cumulative_percent, color='C1', marker='D', ms=7, linestyle='--')
    ax2.set_ylabel('累计百分比', color='C1', fontproperties=font_prop)
    ax2.tick_params(axis='y', labelcolor='C1')

    # 设置次坐标轴的范围
    ax2.set_ylim(0, 100)

    # 显示网格线
    ax1.grid(axis='y')

    # 使用 tight_layout 以防止标签被截断
    plt.tight_layout()

    # 显示图表
    plt.title('影片数量前十的地区的帕累托图', fontproperties=font_prop)
    plt.show()


# 类型分布
def type_analyze(data: pd.DataFrame) -> None:
    """
    柱状统计图；比例饼图；
    :param data:
    :return: None
    """
    print("Type Analyzing...")

    # 预览 data['types'] 数据格式
    print(data['types'])

    # 进行数据拆分和分组
    types_list = []
    for types in data['types']:
        types_list.extend(types)
    types_group = pd.DataFrame(types_list, columns=['type']).groupby('type')

    # 查看各类型影片数
    print(types_group.size())



# 基本信息分析
def found_analysis(data: pd.DataFrame) -> None:
    """
    :param data:
    :return: None
    """
    # (1) 首先查看数值型列的基本统计信息
    print(data.describe())

    # (2) 制片地区分布
    # region_analyze(data)

    # (3) 类型分布
    type_analyze(data)


# data = pd.read_csv('MovieInfo_str.csv', dtype=str)
data = solve_data.data_washing()
# 查看数据集信息
print("Data Info:")
print(data.info(verbose=False))
pd.set_option('display.max_columns', None)  # 设置显示全部列
print(data.head())

found_analysis(data)
