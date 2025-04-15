import os.path
import shutil
import time

from PyQt5.QtGui import QImage

from tools.load import get_ui_path


class ImageItem:

    def __init__(self, source_path = None, relative_name = None):
        if relative_name is None:
            self.relative_name = f"{int(time.time() * 1000)}.png"
        else:
            self.relative_name = relative_name
        if source_path is not None:
            shutil.copy(source_path, os.path.join(get_))
        self.image = QImage()
    def get_relative_path(self):

