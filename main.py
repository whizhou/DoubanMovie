# 将 solve_data.py 合并，进行数据处理，数据分析和可视化

import pandas as pd
import solve_data
import data_analyze


# 基本信息分析
def found_analysis(data: pd.DataFrame) -> None:
    """
    :param data:
    :return: None
    """
    # (1) 首先查看数值型列的基本统计信息
    print(data.describe())

    # (2) 制片地区分布
    data_analyze.region_analyze(data)

    # (3) 类型分布
    data_analyze.type_analyze(data)

    # (4) 影片数量前10的导演 & 影片平均评分前20的导演
    data_analyze.director_analyze(data)


# data = pd.read_csv('MovieInfo_str.csv', dtype=str)
data = solve_data.data_washing()
# 查看数据集信息
print("Data Info:")
print(data.info(verbose=False))
pd.set_option('display.max_columns', None)  # 设置显示全部列
print(data.head())

found_analysis(data)
