import json
import re

# 定义用于去除控制字符的正则表达式
control_chars = re.compile(r'[\x00-\x1F\x7F]')

# 定义函数用于清理控制字符
def remove_control_characters(s):
    return control_chars.sub('', s)

# 初始化空字符串存储清理后的内容
cleaned_content = ''

# 逐行读取并清理文件
with open('input.json', 'r', encoding='gb2312', errors='ignore') as f:
    for line in f:
        cleaned_content += remove_control_characters(line)

# 修复 JSON 转义序列问题
def fix_json_escapes(text):
    # 修复无效的转义序列
    text = re.sub(r'\\([^"\\/bfnrtu])', r'\\\\\1', text)
    return text

# 修复转义序列
cleaned_content = fix_json_escapes(cleaned_content)

# 打印部分内容进行调试
print(cleaned_content[1234170:1234200])  # 打印清理后的前1000个字符以检查是否有问题

# 解析为 JSON 对象
try:
    data = json.loads(cleaned_content)
    print("JSON 文件成功解析")
except json.JSONDecodeError as e:
    print(f"解析 JSON 时出错: {e}")
    # 尝试定位错误位置
    error_pos = e.pos
    start = max(0, error_pos - 50)
    end = min(len(cleaned_content), error_pos + 50)
    print(f"错误位置附近的上下文:\n{cleaned_content[start:end]}")
    exit(1)

# 定义递归函数清理数据中的控制字符
def clean_data(obj):
    if isinstance(obj, str):
        return remove_control_characters(obj)
    elif isinstance(obj, list):
        return [clean_data(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: clean_data(value) for key, value in obj.items()}
    else:
        return obj

# 清理 JSON 数据中的控制字符
cleaned_data = clean_data(data)

# 保存清理后的 JSON 文件
with open('train_2.json', 'w', encoding='utf-8') as f:
    json.dump(cleaned_data, f, ensure_ascii=False, indent=4)