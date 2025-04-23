import matplotlib.pyplot as plt
import numpy as np

# 自定义配色（现代风格）
colors = ['#2878b5', '#9ac9db', '#f8ac8c']  # 绿/橙/蓝
hatch_patterns = ['//', 'xx', '\\\\']        # 不同填充纹理

# 数据配置
categories= ['100', '120', '140']
groups = ['尽力而为', '802.1 Qch', '802.1 Qbv']

data = [
    [135, 158, 187],  # Group1
    [184, 215, 260],  # Group2
    [115, 139, 161]   # Group3
]

# 图形参数
bar_width = 0.2  # 调小柱子宽度
index = np.arange(len(categories)) * 1.2  # 加大类别间距

plt.figure(figsize=(10, 7), dpi=200)

# 绘制每组柱状图
for i, (group, values) in enumerate(zip(groups, data)):
    position = index + i * bar_width
    bars = plt.bar(position, values, bar_width, 
                   color=colors[i],   # 设置颜色
                   edgecolor='black', # 黑色边框
                   hatch=hatch_patterns[i],  # 纹理
                   linewidth=0.8,     # 边框粗细
                   label=group)
    
    # 在柱子上方添加数据标签
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height}',  # 显示数值
                 ha='center', va='bottom',  # 对齐方式
                 fontsize=13)

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False  
# 装饰图表
plt.xlabel('调度流数量', fontsize=18, labelpad=14)
plt.ylabel('最小带宽值（MB）', fontsize=18, labelpad=10)
plt.xticks(index + bar_width, categories, fontsize=14)
plt.yticks(fontsize=14)
plt.legend(title='协议类型', title_fontsize=18, fontsize=14)

# 添加参考线
plt.grid(axis='y', color='gray', linestyle='--', alpha=0.3)

# 优化布局
plt.tight_layout()
plt.show()