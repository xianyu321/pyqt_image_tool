import hashlib
import os.path
import shutil
import time
from platform import release

from PyQt5.QtGui import QImage

from tools.Debug import Debug
from tools.load import get_ui_path, get_static_dir, get_setting_input_images_path
from tools.local_save import generate_file_hash


class ImageItem:


    def __init__(self, source_path = None, relative_name = None):
        if source_path is None and relative_name is None:
            self.image = QImage(16,16, QImage.Format_ARGB32)
            return
        if relative_name is None:
            self.relative_name = f"{generate_file_hash(source_path)}.png"
        else:
            self.relative_name = relative_name
        if source_path is not None:
            try:
                shutil.copy(str(source_path), str(self.get_relative_dir()))
            except FileNotFoundError as e:
                Debug.Error(f"源文件未找到: {e}")
            except PermissionError as e:
                Debug.Error(f"权限错误: {e}")
            except Exception as e:
                Debug.Error(f"发生错误: {e}")
        if source_path is not None or relative_name is not None:
            try:
                self.image = QImage(self.get_relative_dir())
            except Exception as e:
                Debug.Error(f"发生错误: {e}")
    def get_relative_dir(self):
        relative_path = os.path.join(get_setting_input_images_path(), self.relative_name)
        return relative_path



