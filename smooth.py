import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter
from matplotlib.colors import ListedColormap

def read_multi_group_data(filename: str) -> list[np.ndarray]:
    """
    读取多组数据文件，组间用空行分隔
    
    参数:
        filename (str): 数据文件路径
        
    返回:
        list[np.ndarray]: 包含多组数据的列表，每组为一个数组
    
    异常:
        FileNotFoundError: 当文件不存在时抛出
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            groups = []
            current_group = []
            
            for line in f:
                line = line.strip()
                if line:  # 非空行
                    try:
                        current_group.append(float(line))
                    except ValueError:
                        if len(current_group) > 0:
                            groups.append(np.array(current_group))
                            current_group = []
                        continue
                else:  # 空行
                    if len(current_group) > 0:
                        groups.append(np.array(current_group))
                        current_group = []
            
            # 处理最后一组
            if len(current_group) > 0:
                groups.append(np.array(current_group))
                
            if not groups:
                raise ValueError("文件中未找到有效数据组")
                
            return groups
            
    except FileNotFoundError:
        raise FileNotFoundError(f"文件 {filename} 未找到")

def smooth_multi_data(data_groups: list[np.ndarray],
                     window_size: int = 5,
                     method: str = 'savgol') -> list[np.ndarray]:
    """
    批量处理多组数据平滑
    
    参数:
        data_groups: 多组数据列表
        window_size: 奇数窗口大小
        method: 平滑方法 (savgol/moving_avg)
    
    返回:
        平滑后的多组数据列表
    """
    smoothed_groups = []
    
    for idx, data in enumerate(data_groups):
        try:
            if len(data) < window_size:
                raise ValueError(f"第{idx+1}组数据长度({len(data)})小于窗口大小({window_size})")
                
            smoothed = smooth_data(data, window_size, method)
            smoothed_groups.append(smoothed)
            
        except Exception as e:
            print(f"跳过第{idx+1}组: {str(e)}")
            continue
            
    return smoothed_groups

def plot_multi_groups(original_groups: list[np.ndarray],
                     smoothed_groups: list[np.ndarray],
                     title: str = "多组数据平滑分析") -> None:
    """
    绘制多组数据对比图
    
    参数:
        original_groups: 原始数据组列表
        smoothed_groups: 平滑数据组列表
        title: 图表标题
    """
    plt.figure(figsize=(14, 8))
    
    # 使用定性色环（避免颜色重复）
    colors = ListedColormap(['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', 
                            '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']).colors
    
    for idx, (raw, smooth) in enumerate(zip(original_groups, smoothed_groups)):
        color = colors[idx % len(colors)]
        
        # # 绘制原始数据（半透明点）
        # plt.scatter(np.arange(len(raw)) + 1, raw,
                   # alpha=0.3, color=color, s=15,
                   # label=f'组{idx+1} 原始' if idx < 8 else None)
        
        # 绘制平滑曲线
        plt.plot(list(range(10, 1001, 10)), smooth,
                color=color, linewidth=2.5,
                label=f'拓扑图 {idx + 1}' if idx < 8 else None)
    
    # 图表装饰
    plt.xlabel("带宽（MB）", fontsize=25)
    plt.ylabel("运行时间（s）", fontsize=25)
    plt.grid(True, alpha=0.3)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15) 
    # 智能图例显示（超过8组显示颜色条）
    if len(original_groups) <= 8:
        plt.legend(ncol=1, loc='upper right', prop = {"size": 20})
    else:
        # 添加颜色条替代图例
        sm = plt.cm.ScalarMappable(cmap=ListedColormap(colors))
        sm.set_array([])
        cbar = plt.colorbar(sm, aspect=40)
        cbar.set_label('数据组别')
    plt.tight_layout()
    plt.show()

# 复用之前的平滑函数
def smooth_data(data: np.ndarray, 
               window_size: int = 5,
               method: str = 'savgol') -> np.ndarray:
    """
    数据平滑处理
    
    参数:
        data (np.ndarray): 原始数据
        window_size (int): 平滑窗口大小（奇数）
        method (str): 平滑方法 (savgol/moving_avg)
    
    返回:
        np.ndarray: 平滑后的数据
    """
    if window_size % 2 == 0:
        window_size += 1  # 确保窗口大小为奇数
    
    if method == 'savgol':
        # Savitzky-Golay 滤波器
        return savgol_filter(data, window_size, 3)
    elif method == 'moving_avg':
        # 移动平均
        return np.convolve(data, np.ones(window_size)/window_size, mode='valid')
    else:
        raise ValueError("不支持的平滑方法")

# 示例用法
if __name__ == "__main__":
    try:
        # 1. 读取数据文件（修改为实际路径）
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False  
        all_groups = read_multi_group_data("test.result")
        print(f"成功读取 {len(all_groups)} 组数据")
        
        # 2. 执行平滑处理
        smoothed_all = smooth_multi_data(all_groups,
                                        window_size=7,
                                        method='savgol')
        
        # 3. 可视化结果
        plot_multi_groups(all_groups, smoothed_all,
                         title="多组实验数据对比")
    except Exception as e:
        print(f"错误发生: {str(e)}")