import traceback

from enity.Config import SaveConfig
from enity.ImageItem import ImageItem
from tools.Debug import Debug
from tools.local_save import save_json


class ImageManger:
    def __init__(self):
        self.images = []

    def add_image(self, image:ImageItem):
        self.images.append(image)

    def get_image(self, index):
        if index >= len(self.images) or index < 0:
            Debug.Error("错误的索引")
            return None
        return self.images[index]
    def save(self):

        save_json(SaveConfig.input_images, {

        })
