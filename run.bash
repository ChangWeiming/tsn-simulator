#!/bin/bash

total=0
count=10

for ((i=1; i<=$count; i++)); do
    # 执行Python脚本并捕获输出
    result=$(python ./main.py 2>&1)
    
    # 验证输出是否为数字
    if [[ $result =~ ^[+-]?[0-9]+([.][0-9]+)?$ ]]; then
        total=$(echo "$total + $result" | bc)
        echo "第${i}次结果: $result"
    else
        echo "第${i}次出现非数字输出: $result" >&2
        exit 1
    fi
done

# 计算平均值（保留2位小数）
average=$(echo "scale=2; $total / $count" | bc)
echo "最终平均值: $average"