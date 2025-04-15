import os

from PyQt5 import uic
from PyQt5.QtGui import QImage

from enity.Config import StaticConfig
from tools.Setting import Setting


def get_static_dir():
    """获取静态资源的完整路径"""
    # 获取当前脚本所在的目录
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # 构建 static 目录的路径
    static_dir = os.path.join(os.path.dirname(current_dir), "static")
    return static_dir

def get_img_by_name(img_name):
    filepath = get_img_path(img_name)
    with open(filepath, 'rb') as hf:
        data = hf.read()

    image = QImage()
    valid = image.loadFromData(data)
    if not valid:
        return False
    return image

def get_json_dir():
    json_dir = os.path.join(get_static_dir(), StaticConfig.json)
    return json_dir

def get_source_image_dir():
    source_images_dir = os.path.join(get_static_dir(), StaticConfig.source_images)
    return source_images_dir

def get_texture_dir():
    texture_dir = os.path.join(get_static_dir(), StaticConfig.texture)
    return texture_dir

def get_ui_path(ui_file_name):
    """加载指定的 .ui 文件"""
    ui_dir = os.path.join(get_static_dir(), StaticConfig.ui)
    ui_path = os.path.join(ui_dir, ui_file_name)
    return ui_path
def get_img_path(img_name):
    img_dir = os.path.join(get_static_dir(), StaticConfig.img)
    img_path = os.path.join(img_dir, img_name)
    return img_path
def get_ui_img_path(img_name):
    """加载ui图片"""
    ui_dir = os.path.join(get_static_dir(), StaticConfig.ui)
    img_dir = os.path.join(ui_dir, "img")
    img_path = os.path.join(img_dir, img_name)
    return img_path

def get_project_path():
    project_path = os.path.join(get_static_dir(), Setting.name)
    return project_path