# 将 solve_data.py 合并，进行数据处理，数据分析和可视化

import pandas as pd
from datetime import datetime
from matplotlib import pyplot as plt

import solve_data


# TODO Top 250 的制片地区分布
def region_distribution(regions: pd.DataFrame):
    """
    分析对比各地区的影片数
    :param regions:
    :return:
    """
    # print(regions.head())
    print("region-distribution")
    region_group = regions.groupby('region').size()
    print(region_group)

# TODO Top 250 的上映日期分布

# TODO Top 250 的片长分布

# TODO Top 250 的类型分布

# TODO 类型与上映时期，电影评分的关系

# TODO 导演/演员/编剧的评分分析

# TODO Top 250 的导演和演员


# data = pd.read_csv('MovieInfo_str.csv', dtype=str)
data = solve_data.data_washing()
# 查看数据集信息
print("Data Info:")
print(data.info(verbose=False))
pd.set_option('display.max_columns', None)  # 设置显示全部列
print(data.head())


region_distribution(data.regions)
