import json
import re
import chardet

# 定义用于去除控制字符的正则表达式
control_chars = re.compile(r'[\x00-\x1F\x7F]')

# 定义函数用于清理控制字符
def remove_control_characters(s):
    return control_chars.sub('', s)

# 检测文件编码
def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        confidence = result['confidence']
        print(f"检测到编码: {encoding} (置信度: {confidence})")
        
        # 如果置信度较低或检测到二进制编码，尝试常见的中文编码
        if confidence < 0.7 or encoding == 'ascii':
            print("置信度较低，尝试常见中文编码...")
            for enc in ['gbk', 'gb2312', 'utf-8']:
                try:
                    with open(file_path, 'r', encoding=enc) as test_f:
                        test_f.read(1024)  # 尝试读取一部分内容
                    print(f"成功使用编码: {enc}")
                    return enc
                except UnicodeDecodeError:
                    continue
            
            # 如果所有编码都失败，返回检测到的编码
            return encoding if encoding else 'gbk'
        
        return encoding

# 检测文件编码
file_encoding = detect_encoding('input.json')

# 初始化空字符串存储清理后的内容
cleaned_content = ''

# 逐行读取并清理文件
try:
    with open('input.json', 'r', encoding=file_encoding) as f:
        for line in f:
            cleaned_content += remove_control_characters(line)
except UnicodeDecodeError:
    print(f"使用编码 {file_encoding} 读取失败，尝试备用编码...")
    # 尝试常见的中文编码
    for enc in ['gbk', 'gb2312', 'utf-8']:
        if enc == file_encoding:
            continue
        try:
            with open('input.json', 'r', encoding=enc) as f:
                cleaned_content = ''
                for line in f:
                    cleaned_content += remove_control_characters(line)
            print(f"成功使用备用编码: {enc}")
            break
        except UnicodeDecodeError:
            continue
    else:
        print("无法读取文件，所有编码尝试均失败")
        exit(1)

# 打印部分内容进行调试
print(cleaned_content[1234170:1234200])  # 打印清理后的部分字符以检查是否有问题

# 解析为 JSON 对象
try:
    data = json.loads(cleaned_content)
    print("JSON 文件成功解析")
except json.JSONDecodeError as e:
    print(f"解析 JSON 时出错: {e}")
    print("尝试修复常见的 JSON 格式问题...")
    
    # 尝试修复常见的 JSON 格式问题
    try:
        # 尝试处理单引号问题
        cleaned_content = cleaned_content.replace("'", '"')
        # 尝试处理尾随逗号
        cleaned_content = re.sub(r',\s*}', '}', cleaned_content)
        cleaned_content = re.sub(r',\s*]', ']', cleaned_content)
        
        data = json.loads(cleaned_content)
        print("JSON 文件成功解析（修复后）")
    except json.JSONDecodeError as e2:
        print(f"修复后仍然出错: {e2}")
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

# 保存清理后的 JSON 文件（使用 UTF-8 编码）
with open('train.json', 'w', encoding='utf-8') as f:
    json.dump(cleaned_data, f, ensure_ascii=False, indent=4)

print("文件清洗完成，已保存为 train.json（UTF-8 编码）")