# 进阶数据分析模块
import pandas as pd
import networkx as nx
from matplotlib import pyplot as plt
import matplotlib.font_manager as fm

# 设置中文字体
font_path = 'SimHei.ttf'  # 替换为实际字体文件的路径
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.sans-serif'] = [font_prop.get_name()]
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


# 导演-编剧 & 导演-演员的合作关系
def collaboration(data: pd.DataFrame):
    """
    绘制网络图,边的粗细由合作次数决定
    使用 networkx 和 matplotlib 库绘制网络图
    :param data:
    :return:
    """
    print("Collaboration Analyzing...")

    """
    统计导演-编剧合作关系
    """
    # 进行数据拆分
    director_writer_list = []
    for director, writers in zip(data['director'], data['writers']):
        director_writer_list.extend([[director, writer] for writer in writers])
    director_writer_df = pd.DataFrame(director_writer_list, columns=['director', 'writer'])

    # 统计导演-编剧合作次数
    director_writer_count = director_writer_df.groupby(['director', 'writer']).size().reset_index(name='count')
    director_writer_sorted = director_writer_count.sort_values(by='count', ascending=False)
    print(director_writer_sorted.head(20))

    # 创建有向图
    G = nx.DiGraph()

    # 添加节点和边
    for _, row in director_writer_sorted.head(10).iterrows():
        G.add_edge(row['director'], row['writer'], weight=row['count'])

    # 设置节点布局
    pos = nx.spring_layout(G)

    # 绘制网络图
    plt.figure()

    # 根据权重绘制边
    edges = G.edges(data=True)
    for u, v, d in edges:
        nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], width=d['weight'], alpha=0.6)

    # 添加边权重标签
    edge_labels = {(u, v): d['weight'] for u, v, d in edges}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # 绘制节点和标签
    nx.draw_networkx_nodes(G, pos, node_size=1500, node_color='skyblue')
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')

    # 显示图标
    plt.title("导演-编剧合作关系网络图")
    plt.show()

    """
    统计导演-演员合作关系
    """
    # 进行数据拆分
    director_actor_list = []
    for director, actors in zip(data['director'], data['actors']):
        director_actor_list.extend([[director, actor] for actor in actors])
    director_actor_df = pd.DataFrame(director_actor_list, columns=['director', 'actor'])

    # 统计导演-编剧合作次数
    director_actor_count = director_actor_df.groupby(['director', 'actor']).size().reset_index(name='count')
    director_actor_sorted = director_actor_count.sort_values(by='count', ascending=False)
    print(director_actor_sorted.head(15))

    # 创建有向图
    G = nx.DiGraph()

    # 添加节点和边
    for _, row in director_actor_sorted.head(10).iterrows():
        G.add_edge(row['director'], row['actor'], weight=row['count'])

    # 设置节点布局
    pos = nx.spring_layout(G)

    # 绘制网络图
    plt.figure()

    # 根据权重绘制边
    edges = G.edges(data=True)
    for u, v, d in edges:
        nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], width=d['weight'], alpha=0.6, arrows=True, arrowsize=30)

    # 添加边权重标签
    edge_labels = {(u, v): d['weight'] for u, v, d in edges}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # 绘制节点和标签
    nx.draw_networkx_nodes(G, pos, node_size=1500, node_color='skyblue')
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')

    # 显示图标
    plt.title("导演-演员合作关系网络图")
    plt.show()
