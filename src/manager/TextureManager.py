import math
import os.path

from PyQt5.QtGui import QImage, QPainter

from enity.ImageItem import ImageItem
from manager.EventManager import EventManager
from manager.ImagesManager import ImagesManager
from tools.load import get_setting_path, get_setting_texture_path


class TextureManager:
    _instance = None  # 单例实例
    texture_size = 16
    packer_size = 10
    def __new__(cls, *args, **kwargs):
        """
        实现单例模式
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    def __init__(self, file_name = None):
        self.img_map = {}
        self.file_name = "texture.png"
        self.texture_image = None

    @staticmethod
    def get_instance():
        """
        获取单例实例
        """
        if TextureManager._instance is None:
            TextureManager()
        return TextureManager._instance
    def add_item(self, rol:int, col:int, item: ImageItem):
        return
    def pixel_address(self, rol, col):
        return rol * self.texture_size, col * self.texture_size

    def get_file_dir(self):
        file_dir = os.path.join(get_setting_texture_path(), self.file_name)
        return file_dir

    def add_tex(self, index, num = 1):
        if index is None:
            return
        current_value = self.img_map.get(index, 0)
        if current_value is None:
            current_value = 0
        new_value = current_value + num
        self.img_map[index] = new_value
        e:EventManager = EventManager.get_instance()
        e.emit("update_texture")
    def reduce_txe(self, index, num = 1):
        if index is None:
            return
        self.img_map[index] -= num
        if self.img_map[index] == 0:
            del self.img_map[index]
        e:EventManager = EventManager.get_instance()
        e.emit("update_texture")

    def get_all_tex(self):
        tex_list = []
        image_manager:ImagesManager = ImagesManager.get_instance()
        for index in self.img_map.keys():
            tex_list.append(image_manager.get_q_image(index))
        return tex_list
    def export_all(self):
        num_items = len(self.img_map)
        self.packer_size = math.ceil(math.sqrt(num_items))
        size = self.texture_size * self.packer_size
        self.texture_image = QImage(size, size, QImage.Format_ARGB32)
        texture_painter = QPainter(self.texture_image)
        for i, item in enumerate(self.img_map.keys()):
            rol = i // self.packer_size  # 计算行数
            col = i % self.packer_size  # 计算列数
            x, y = self.pixel_address(rol, col)
            image_manager: ImagesManager = ImagesManager.get_instance()
            img = image_manager.get_q_image(item)
            texture_painter.drawImage(y, x, img)
        self.texture_image.save(self.get_file_dir(), "PNG")
