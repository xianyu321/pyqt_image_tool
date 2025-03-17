import os

from PyQt5 import uic
from PyQt5.QtGui import QImage


def get_static_dir():
    """获取静态资源的完整路径"""
    # 获取当前脚本所在的目录
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # 构建 static 目录的路径
    static_dir = os.path.join(os.path.dirname(current_dir), "static")
    return static_dir

def get_ui_path(ui_file_name):
    """加载指定的 .ui 文件"""
    # 构建 .ui 文件的完整路径
    ui_dir = os.path.join(get_static_dir(), "ui")
    ui_path = os.path.join(ui_dir, ui_file_name)
    return ui_path

def get_img_path(img_name):
    img_dir = os.path.join(get_static_dir(), "img")
    img_path = os.path.join(img_dir, img_name)
    return img_path

def get_img_by_name(img_name):
    filepath = get_img_path(img_name)
    with open(filepath, 'rb') as hf:
        data = hf.read()

    image = QImage()
    valid = image.loadFromData(data)
    if not valid:
        return False
    return image
