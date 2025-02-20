import subprocess
import os
import pandas as pd
import time
import re

def extract_mermaid_code(text):
    """
    从文本中提取 Mermaid 代码块。
    :param text: 包含 Mermaid 代码块的文本
    :return: 提取到的 Mermaid 代码块，如果未找到则返回输入的文本
    """
    start_tag = "```mermaid"
    end_tag = "```"
    start_index = text.find(start_tag)
    if start_index == -1:
        return text
    start_index += len(start_tag)
    end_index = text.find(end_tag, start_index)
    if end_index == -1:
        return text
    mermaid_code = text[start_index:end_index].strip()
    # 清理无效字符，例如 HTML 标签
    mermaid_code = re.sub(r'<[^>]+>', '', mermaid_code)
    full_mermaid_code = f'mermaid\n{mermaid_code}\n'
    return full_mermaid_code

def mermaid_to_image(mermaid_code, output_file, output_format="png"):
    """
    将Mermaid代码转换为图片。

    参数:
        mermaid_code (str): Mermaid代码。
        output_file (str): 输出文件的路径（不需要扩展名）。
        output_format (str): 输出图片的格式，支持 "png"、"svg"、"pdf" 等，默认为 "png"。
    """
    # 确保输出文件路径的目录存在
    os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)

    # 将Mermaid代码写入临时文件
    temp_mmd_file = "temp.mmd"
    with open(temp_mmd_file, "w", encoding="utf-8") as f:
        f.write(mermaid_code)

    # 调用mmdc命令行工具
    command = [
        "mmdc",  # mermaid-cli的命令
        "-i", temp_mmd_file,  # 输入文件
        "-o", f"{output_file}.{output_format}",  # 输出文件
        "-t", "default",  # 主题（可选）
        "-b", "white"  # 背景颜色（可选）
    ]

    try:
        # 执行命令
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # 检查命令是否成功执行
        if result.returncode == 0:
            print(f"图片已成功生成: {output_file}.{output_format}")
        else:
            print(f"生成图片失败: {result.stderr}")
    except FileNotFoundError:
        print("未找到 mmdc 命令，请确保已安装 mermaid-cli。")
    finally:
        # 删除临时文件
        if os.path.exists(temp_mmd_file):
            os.remove(temp_mmd_file)

# 读取Excel文件
# file_path = "./mermaid_chart.xlsx"
file_path = "./ds_r1_result.xlsx"
sheet_name = 'Sheet1'
df = pd.read_excel(file_path, sheet_name=sheet_name)
# 读取第三列的数据
query = df.iloc[:, 0]
reference_content = df.iloc[:, 1]
content = df.iloc[:, 2]

for i in range(len(query)):
    query_item = query[i]
    reference_content_item = reference_content[i]
    content_item = content[i]
    if(not content_item):
        print(f"{query_item[:max(len(query_item),10)]} 没有内容")
        continue
    mermaid_code = extract_mermaid_code(content_item)
    mermaid_to_image(mermaid_code, f"./mermaid_images_r1/{query_item[:max(len(query_item),50)]}", output_format="png")