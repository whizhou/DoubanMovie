# 关联性数据分析模块
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.font_manager as fm

# 设置中文字体
font_path = 'SimHei.ttf'  # 替换为实际字体文件的路径
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.sans-serif'] = [font_prop.get_name()]
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


# 上映年份-影片数量
def year_movies(data: pd.DataFrame):
    """
    按年份统计每年的电影数量
    上映年份-影片数量折线图展示
    :param data:
    :return:
    """
    print("Year-Movies Analyzing...")

    # 数据分组统计
    year_group = data.groupby('year')
    year_count = year_group.size()

    print(year_count)

    # 绘制每年的电影数量折线图
    year_count.plot()
    plt.title("按年份统计每年的电影数量")
    plt.xlabel("年份")
    plt.ylabel("当年电影数量")
    plt.grid(alpha=0.3, linestyle='--')
    plt.show()

    # 绘制电影数量逐年累加折线图
    year_count.cumsum().plot()
    plt.title("逐年电影累计数量")
    plt.xlabel("年份")
    plt.ylabel("累计电影数量")
    plt.grid(alpha=0.3, linestyle='--')
    plt.show()


# 类型-评分-评分人数综合分析
def types_rating_people(data: pd.DataFrame):
    """
    类型-评分-评分人数综合分析
    :param data:
    :return:
    """
    print("Types-Rating-Rating_People Analyzing...")

    # 绘制散点图
    plt.scatter(data['rating'], data['rating_people'])
    plt.show()
