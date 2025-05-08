import hashlib
import json
import os

from tools.Debug import Debug
from tools.load import get_json_dir

def save_json_by_name(file_name, data):
    # 将每个方块转换为字典格式
    # 将数据保存到文件
    with open(os.path.join(get_json_dir(), file_name), "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    Debug.Log(f"成功保存到 {file_name} 中")
def load_json_by_name(file_name):
    try:
        with open(os.path.join(get_json_dir(), file_name), "r", encoding="utf-8") as file:
            data = json.load(file)
        # 将字典数据转换为 Block 对象
        Debug.Log(f"成功读取 {file_name} 文件")
    except FileNotFoundError:
        Debug.Error(f"文件未找到：{file_name}")
    except json.JSONDecodeError:
        Debug.Error(f"文件内容不是有效的 JSON 格式：{file_name}")
    return data

def load_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        # 将字典数据转换为 Block 对象
        Debug.Log(f"成功读取 {file_path} 文件")
    except FileNotFoundError:
        Debug.Error(f"文件未找到：{file_path}")
    except json.JSONDecodeError:
        Debug.Error(f"文件内容不是有效的 JSON 格式：{file_path}")
    return data

def save_json(file_path, data):
    # 将每个方块转换为字典格式
    # 将数据保存到文件
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    Debug.Log(f"成功保存到 {file_path} 中")

def generate_file_hash(file_path, hash_algorithm='sha256'):
    hash_func = hashlib.new(hash_algorithm)
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)
    return hash_func.hexdigest()