import os


from enity.Config import SaveConfig, JsonConfig
from enity.ImageItem import ImageItem
from models.MoveLabel import MoveLabel
from tools.Debug import Debug
from tools.load import get_setting_input_images_path
from tools.local_save import save_json, load_json


class ImagesManager:
    _instance = None  # 单例实例

    def __new__(cls, *args, **kwargs):
        """
        实现单例模式
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    def __init__(self):
        self.images = []
        self.widget = None
    @staticmethod
    def get_instance():
        """
        获取单例实例
        """
        if ImagesManager._instance is None:
            ImagesManager()
        return ImagesManager._instance
    def set_widget(self, widget):
        self.widget = widget

    def contains_item(self, image:ImageItem):
        for item in self.images:
            if image.relative_name == item.relative_name:  # 检查对象的 id 属性是否匹配
                return True
        return False

    def add_image(self, image:ImageItem):
        if self.contains_item(image):
            Debug.Log("重复的文件")
            return
        label = MoveLabel(image=image.image)
        label.set_image_index(len(self.widget.move_labels))
        self.widget.add_item(len(self.widget.move_labels), label)
        self.images.append(image)
        self.save_to_json()
    def add_image_by_copy(self, path):
        image_item = ImageItem(source_path=path)
        self.add_image(image_item)
        return image_item

    def init_image_by_json(self):
        file_json = self.open_by_json()
        for file_name in file_json:
            image_item = ImageItem(relative_name=file_name)
            self.images.append(image_item)
    def get_image(self, index):
        if index >= len(self.images) or index < 0:
            Debug.Error("错误的索引")
            return None
        return self.images[index]

    def get_q_image(self, index):
        if index is None:
            return
        image_item = self.get_image(index)
        if image_item is None:
            return None
        return image_item.image
    def get_json_dir(self):
        images_path = get_setting_input_images_path()
        json_dir = os.path.join(images_path, JsonConfig.images)
        return json_dir
    def save_to_json(self):
        json_data = []
        for item in self.images:
            json_data.append(item.relative_name)
        save_json(self.get_json_dir(), json_data)
    def open_by_json(self):
        file_path = self.get_json_dir()
        if not os.path.isfile(file_path):
            self.save_to_json()
        file_json = load_json(file_path)
        return file_json