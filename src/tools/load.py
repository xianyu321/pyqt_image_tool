import os

from PyQt5 import uic
from PyQt5.QtGui import QImage

from enity.Config import StaticConfig, OutputConfig
from tools.Setting import Setting

def get_project_path():
    project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return project_path

def get_static_dir():
    static_dir = os.path.join(get_project_path(), StaticConfig.static)
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

def get_setting_path():
    output_path = os.path.join(get_project_path(), OutputConfig.output)
    setting_path = os.path.join(output_path, Setting.name)
    ensure_directory_exists(setting_path)
    return setting_path

def get_setting_input_images_path():
    input_images_dir = os.path.join(get_setting_path(), OutputConfig.images)
    ensure_directory_exists(input_images_dir)
    return input_images_dir

def ensure_directory_exists(directory_path):
    """
    检查文件夹是否存在，如果不存在则创建。
    :param directory_path: 文件夹路径
    """
    if not os.path.exists(directory_path):
        print(f"文件夹不存在，正在创建: {directory_path}")
        os.makedirs(directory_path)  # 递归创建目录

