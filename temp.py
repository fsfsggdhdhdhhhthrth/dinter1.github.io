import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

# 创建一个空的无向图
G = nx.Graph()

# 从Excel文件加载数据
excel_file = "/Users/yuntech/Desktop/ＬＥＯ/CADVis_Author.xlsx"  # 替换为您的Excel文件路径
df = pd.read_excel(excel_file)

# 根据相同的 work_id 创建节点和边
for work_id, group in df.groupby("work_id"):
    authors = group["Fullname"].tolist()
    order = group["Order"].tolist()
    
    # 添加节点（作者）
    for author in authors:
        G.add_node(author)  # 添加节点（作者）
    
    # 添加带有作者顺序的边（合作关系）
    for i in range(len(authors)):
        for j in range(i + 1, len(authors)):
            G.add_edge(authors[i], authors[j], order=order[i])  # 使用order[i]来表示作者顺序

# 创建一个子图，只包括与Marc Aurel Schnabel相关的节点和边
subgraph = G.subgraph(["Marc Aurel Schnabel"] + list(G.neighbors("Marc Aurel Schnabel")))

# 计算节点的度中心性
degree_centrality = nx.degree_centrality(subgraph)

# 计算节点的大小，根据度中心性调整
node_size = [300 * degree_centrality[node] for node in subgraph.nodes()]

# 可视化SNA图
plt.figure(figsize=(12, 12))

# 自定义布局
pos = nx.spring_layout(subgraph, seed=42)

# 绘制边，根据作者顺序添加不同颜色的边（浅色系）
for edge in subgraph.edges(data=True):
    order = edge[2]["order"]
    if order == 1:
        edge_color = "lightcoral"  # 浅红色
    elif order == 2:
        edge_color = "lightblue"  # 浅蓝色
    elif order == 3:
        edge_color = "lightgreen"  # 浅绿色
    else:
        edge_color = "lightgray"  # 浅灰色
    nx.draw_networkx_edges(subgraph, pos, edgelist=[(edge[0], edge[1])], edge_color=edge_color, width=2)

# 绘制节点，节点大小基于度中心性，节点颜色为芥末色
nx.draw(subgraph, pos, node_size=node_size, node_color='#A4C639', with_labels=False, edgecolors='black', linewidths=0.5)

# 绘制节点标签（度中心性），但调整它们的位置以避免重叠，并设置文字颜色为深黑色
label_pos = {k: (v[0], v[1] - 0.02) for k, v in pos.items()}
labels = {node: f"{node}\nDegree Centrality: {degree_centrality[node]:.2f}" for node in subgraph.nodes()}
nx.draw_networkx_labels(subgraph, label_pos, labels=labels, font_size=8, font_color='#000000')

plt.title("Collaboration Network (SNA) Graph with Author Order (Marc Aurel Schnabel)")
plt.axis('off')  # 关闭坐标轴
plt.show()
