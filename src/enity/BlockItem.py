from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage

from manager.ImagesManager import ImagesManager


class BlockItem:
    text_img = QImage(16, 16, QImage.Format_ARGB32)
    text_img.fill(Qt.red)
    def __init__(self, name, left=None, right=None, front=None, back=None, up=None, down=None):
        self.name = name
        self.faces = {
            "left" : left,
            "right": right,
            "front": front,
            "back": back,
            "up": up,
            "down": down
        }
        self.face_textures = {}

        for key, value in self.faces.items():
            if value is None:
                self.face_textures[key] = self.text_img
            else:
                img = ImagesManager.get_instance().get_q_image(value)
                self.face_textures[key] = img
    def set_face(self, face, data):
        """
        设置某个面的数据。

        :param face: 面的名称（如 "top", "bottom", "front" 等）
        :param data: 要设置的数据
        """
        if face in self.faces:
            self.faces[face] = data
        else:
            raise ValueError(f"无效的面名称：{face}。有效名称为：{list(self.faces.keys())}")

    def to_dict(self):
        """
        将方块对象转换为字典格式，便于序列化。
        """
        return {
            "name": self.name,
            "faces": self.faces
        }

    @staticmethod
    def from_dict(data):
        """
        从字典格式创建一个方块对象。

        :param data: 包含方块信息的字典
        :return: Block 对象
        """
        name = data.get("name")
        faces = data.get("faces", {})
        block = BlockItem(name)
        block.faces = faces
        return block

    def __str__(self):
        """
        返回方块的字符串表示。
        """
        return f"Block(name={self.name}, faces={self.faces})"