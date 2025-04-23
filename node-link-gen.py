import random
from typing import List, Tuple

def generate_topology(num_nodes: int, num_links: int) -> List[Tuple[int, int]]:
    """
    生成随机无向图拓扑结构
    
    参数:
        num_nodes (int): 节点数量 (≥2)
        num_links (int): 链路数量 (0 ≤ links ≤ n(n-1)/2)
    
    返回:
        List[Tuple[int, int]]: 无向边列表，节点编号从0开始
    
    异常:
        ValueError: 当输入参数不合法时抛出
    """
    # 验证节点数量
    if num_nodes < 2:
        raise ValueError("节点数量至少需要2个")
    
    # 计算最大可能链路数
    max_possible_links = num_nodes * (num_nodes - 1) // 2
    
    # 验证链路数量
    if num_links < 0 or num_links > max_possible_links:
        raise ValueError(f"链路数量应在0到{max_possible_links}之间")

    # 生成节点集合
    nodes = list(range(num_nodes))
    
    # 使用集合存储边以避免重复
    edges = set()
    
    # 当需要生成超过50%的可能链路时，采用补集优化策略
    if num_links > max_possible_links // 2:
        # 生成所有可能的边
        all_edges = {(i, j) for i in nodes for j in nodes if i < j}
        # 随机移除边直到剩余指定数量
        edges = set(random.sample(list(all_edges), num_links))
    else:
        # 常规模式：随机添加边
        while len(edges) < num_links:
            # 随机选择两个不同节点
            u, v = random.sample(nodes, 2)
            # 标准化边表示 (排序后元组)
            edge = (u, v) if u < v else (v, u)
            edges.add(edge)
    
    return list(edges)

def print_topology(node, link, edges: List[Tuple[int, int]]) -> None:
    with open(f"data/runtime-topo/link.{node}.{link}.topo", "w+") as f:
        for u, v in edges:
            f.write(f"{u} {v}\n")

# 示例用法
if __name__ == "__main__":
    try:
        for i in [22, 25, 28]:
            for j in range(8, 14):
                topology = generate_topology(j, i)
                print_topology(j, i, topology)
    except ValueError as e:
        print(f"参数错误：{e}")