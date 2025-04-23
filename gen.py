import random

def generate_topology(num_nodes, connection_prob=0.4):
    """生成随机拓扑图
    参数：
        num_nodes: 节点数量 
        connection_prob: 两节点间的连接概率（默认0.4）
    返回：
        边列表，格式如 [(0, 1), (1, 2), ...]
    """
    edges = []
    # 遍历所有可能的节点对（无向图，i < j避免重复）
    for i in range(num_nodes):
        for j in range(i+1, num_nodes):
            if random.random() < connection_prob:
                edges.append((i, j))
    return edges

# 示例使用
if __name__ == "__main__":
    # 生成拓扑
    num_nodes = 10
    topology = generate_topology(num_nodes)
    
    # 文本输出
    # print(f"节点数量：{num_nodes}")
    # print("边列表：")
    print(len(topology))
    with open(f"{len(topology)}.topo", "w+") as f:
        for edge in topology:
            # print(edge[0], edge[1])
            f.write(f"{edge[0]} {edge[1]}\n")

    # 可视化（需要安装networkx和matplotlib）
    try:
        exit()
        # print ("visual")
        import networkx as nx
        import matplotlib.pyplot as plt
        
        # 创建图对象
        G = nx.Graph()
        G.add_edges_from(topology)
        
        # 绘制图形
        plt.figure(figsize=(8, 6))
        nx.draw(G, 
                with_labels=True,
                node_color='skyblue',
                node_size=800,
                edge_color='gray',
                pos=nx.spring_layout(G))
        plt.title("随机拓扑图")
        plt.savefig('test.png')
        plt.show()
    except ImportError:
        print("\n提示：安装可视化库可查看图形")
        print("pip install networkx matplotlib")