import os
import traceback

from enity.Config import SaveConfig
from enity.ImageItem import ImageItem
from tools.Debug import Debug
from tools.load import get_setting_input_images_path
from tools.local_save import save_json


class ImagesManager:
    def __init__(self):
        self.images = []

    def add_image(self, image:ImageItem):
        self.images.append(image)
    def add_image_by_copy(self, path):
        image_item = ImageItem(source_path=path)
        self.images.append(image_item)

    def init_image_by_path(self):
        images_path = get_setting_input_images_path()
        for file_name in os.listdir(images_path):
            image_item = ImageItem(relative_name=file_name)
            self.images.append(image_item)

    def get_image(self, index):
        if index >= len(self.images) or index < 0:
            Debug.Error("错误的索引")
            return None
        return self.images[index]
    def save_to_json(self):
        save_json(SaveConfig.input_images, {

        })
images_manager = ImagesManager()
images_manager.init_image_by_path()