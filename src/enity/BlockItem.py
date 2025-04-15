class BlockItem:
    def __init__(self, name, top=None, bottom=None, front=None, back=None, left=None, right=None):
        """
        初始化一个方块对象。

        :param name: 方块的名字
        :param top: 顶面数据（默认为 None）
        :param bottom: 底面数据（默认为 None）
        :param front: 前面数据（默认为 None）
        :param back: 后面数据（默认为 None）
        :param left: 左侧面数据（默认为 None）
        :param right: 右侧面数据（默认为 None）
        """
        self.name = name
        self.faces = {
            "top": top,
            "bottom": bottom,
            "front": front,
            "back": back,
            "left": left,
            "right": right
        }

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