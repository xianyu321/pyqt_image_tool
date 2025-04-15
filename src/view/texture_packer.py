import os
from time import sleep

from PyQt5 import uic
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QWidget, QGridLayout, QApplication, QPushButton, QVBoxLayout

# from view.block_item import ToolBar3D
from view.main_widget import GLWidget
from models.ImageMoveWidget import ImageMoveWidget
from tools.load import get_ui_path, get_texture_dir


class TexturePacker(QWidget):
    texture_box: QGridLayout
    input_image_box: QGridLayout
    block_box: QGridLayout
    input_image_btn: QPushButton
    output_image_btn: QPushButton
    textures = []
    input_images = []
    blocks = []
    input_image_widget: ImageMoveWidget
    texture_widget: ImageMoveWidget
    main_widget: QWidget

    def __init__(self):
        super().__init__()
        uic.loadUi(get_ui_path('texture.ui'), self)
        self.box_width = 64  # 固定子框的宽度
        self.box_height = 64  # 固定子框的高度
        self.input_image_btn.clicked.connect(self.add_box)
        self.gl_widget = GLWidget(self.main_widget)
        # self.gl_widget = ToolBar3D(self.main_widget)
        layout = QVBoxLayout(self.main_widget)
        layout.addWidget(self.gl_widget)

    def show(self):

        super().show()
        self.init_data()

    def init_data(self):
        folder_path = get_texture_dir()
        file_name_arr = []
        if folder_path:
            # 清空列表
            file_name_arr.clear()
            # 获取文件夹内的所有文件名，并添加到列表中
            for file_name in os.listdir(folder_path):
                file_name_arr.append(file_name)
        for file_name in file_name_arr:
            image = QImage(os.path.join(folder_path, file_name))
            self.input_images.append(image)
        self.input_image_widget.init_box(self.input_images)
        # self.texture_widget.init_box()
        return

    def add_box(self):
        return
    def onInputImageBtnClicked(self):
        print('input image btn clicked')

if __name__ == '__main__':
    app = QApplication([])
    ex = TexturePacker()
    ex.show()
    app.exec_()

