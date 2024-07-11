import json

# 读取原始的json文件
with open('app.json', 'r') as file:
    data = json.load(file)

# 在每个元素中加入deadline字段
for item in data:
    item['start_time'] = 0

# 输出到新文件app.json.new
with open('app.json', 'w') as file:
    json.dump(data, file)