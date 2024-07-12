import json

# 定义一个函数来处理文件转换
def convert_to_json(file_path, output_file, time:str):
    data = {
            'last_modified_time':[time],
            'members':None
        }
    with open(file_path, 'r') as file:  # 打开文件进行读取
        for line_number, line in enumerate(file, start=1):  # 遍历文件的每一行
            try:
                wechat_id, record, name = line.strip().split('\t')  # 分割每一行的数据
            except ValueError:
                print(f"Invalid data: {line_number:}{line}")
                continue
            # 将数据转换为字典格式，并添加到列表中
            data['members'].append({
                "wechat_id": wechat_id,
                "record": int(record),  # 确保record是整数类型
                "name": name
            })
    
    # 将列表数据转换为JSON格式，并写入到输出文件中
    with open(output_file, 'w') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)  # 美化输出

# 调用函数，传入源文件路径和输出文件路径
convert_to_json('data.txt', 'setting/guarantee_data.json', time = '2024年6月30日')