import subprocess
import re
import sys
from typing import Optional
import json
import os
from typing import Dict, Any

import json
import os
from typing import Dict, Any

def modify_json_fields(file_path: str, updates: Dict[str, str]) -> None:
    """
    原子化修改JSON文件中的多个字段
    
    :param file_path: JSON文件路径
    :param updates: 需要修改的字段字典 {字段名: 新值}
    """
    # 前置校验
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"目标文件 {file_path} 不存在")
    if not all(updates.values()):
        raise ValueError("新值不能为空")

    with open(file_path, 'r+', encoding='utf-8') as f:
        try:
            data: Dict[str, Any] = json.load(f)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"文件解析失败: {e.msg}", e.doc, e.pos) from e

        # 保存原始值用于回滚
        original_values = {}
        for key in updates:
            if key not in data:
                raise KeyError(f"字段 {key} 不存在于JSON结构中")
            original_values[key] = data[key]

        # 更新内存中的数据
        for key, value in updates.items():
            data[key] = value

        # 原子化写入
        try:
            f.seek(0)
            json.dump(data, f, indent=4, ensure_ascii=False)
            f.truncate()
        except Exception as e:
            # 恢复原始数据
            for key in original_values:
                data[key] = original_values[key]
            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=4, ensure_ascii=False)
            raise RuntimeError("写入失败，已恢复原始数据") from e

def run_main(num_runs: int = 10) -> Optional[float]:
    total = 0.0
    success_count = 0
    
    # 数字匹配正则（支持科学计数法）
    number_pattern = re.compile(r'^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$')

    for i in range(1, num_runs + 1):
        try:
            # 执行命令并捕获输出
            result = subprocess.run(
                [sys.executable, 'main.py'],
                check=True,
                capture_output=True,
                text=True,
                timeout=10000  # 设置超时时间（秒）
            )
            
            output = result.stdout.strip()
            
            # 验证输出格式
            if not number_pattern.match(output):
                print(f"第 {i} 次执行 - 错误: 非数字输出 '{output}'")
                continue
                
            # 类型转换
            value = float(output)
            total += value
            success_count += 1
            # print(f"第 {i} 次结果: {value:.4f}")
            
        except subprocess.CalledProcessError as e:
            print(f"第 {i} 次执行 - 错误: 进程返回 {e.returncode}\n错误信息: {e.stderr.strip()}")
        except subprocess.TimeoutExpired:
            print(f"第 {i} 次执行 - 错误: 执行超时")
        except Exception as e:
            print(f"第 {i} 次执行 - 未知错误: {str(e)}")
    
    if success_count == 0:
        print("错误: 所有执行均失败")
        return None
        
    average = total / success_count
    # print(f"\n成功执行次数: {success_count}/{num_runs}")
    # print(f"总和: {total:.4f}")
    print(average)
    return average

if __name__ == "__main__":
    # 从命令行参数读取执行次数（默认10次）
    try:
        runs = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    except ValueError:
        print("错误: 参数必须是整数")
        sys.exit(1)
        
    for i in range(1, 6):
        print(f"topo {i}")
        for j in range(10, 1001, 10):
            modify_json_fields('data/config.json', {
                "topo_map_path": f"data/{i}.topo",
                "app_path": f"data/{i}.topo.bandwitdth.json",
                "switch_num": 10,
                "simulation_time_ms": 32,
                "bandwidth_mb": j,
            })
            result = run_main(runs)
            if result is None:
                raise RuntimeError
    # sys.exit(0 if result is not None else 1)