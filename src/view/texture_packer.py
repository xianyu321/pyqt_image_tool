import os
from time import sleep

from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QWidget, QGridLayout, QApplication, QPushButton, QVBoxLayout, QGroupBox, QScrollArea
from PyQt5.uic import loadUi

from manager.ImagesManager import ImagesManager
# from view.block_item import ToolBar3D
from view.main_widget import GLWidget
from models.ImageMoveWidget import ImageMoveWidget
from tools.load import get_ui_path, get_texture_dir


class TexturePacker(QWidget):

    def __init__(self):
        super().__init__()
        self.textures = []
        self.input_images = []
        self.images_manager = ImagesManager()
        self.blocks = []
        # self.scrollArea_4:QScrollArea
        # self.texture_widget: ImageMoveWidget
        # self.texture_box: QGridLayout
        # self.input_image_box: QGridLayout
        # self.block_box: QGridLayout
        # self.input_image_btn: QPushButton
        # self.output_image_btn: QPushButton
        # self.main_widget: QWidget
        loadUi(get_ui_path('texture.ui'), self)
        self.groupBox_2:QGroupBox = self.findChild(QGroupBox, "groupBox_2")
        self.input_image_widget:ImageMoveWidget = self.findChild(ImageMoveWidget, "input_image_widget")
        self.scroll_input: QScrollArea = self.findChild(QScrollArea, "scroll_input")
        self.scroll_texture: QScrollArea = self.findChild(QScrollArea, "scroll_texture")
        self.input_image_btn.clicked.connect(self.add_box)

        self.gl_widget = GLWidget(self.main_widget)
        layout = QVBoxLayout(self.main_widget)
        layout.addWidget(self.gl_widget)
    def init_width(self):
        # 添加方框线的宽度
        width = self.input_image_widget.getwidth() + self.groupBox_2.contentsMargins().left() + self.groupBox_2.contentsMargins().right()
        self.scroll_input.setFixedWidth(width)
        self.scroll_texture.setFixedWidth(width)


    def show(self):
        super().show()
        self.init_data()
        self.init_width()

    def init_data(self):
        folder_path = get_texture_dir()
        file_name_arr = []
        self.images_manager.init_image_by_path()
        print(len(self.images_manager.images))
        # if folder_path:
        #     # 清空列表
        #     file_name_arr.clear()
        #     # 获取文件夹内的所有文件名，并添加到列表中
        #     for file_name in os.listdir(folder_path):
        #         file_name_arr.append(file_name)
        # for file_name in file_name_arr:
        #     image = QImage(os.path.join(folder_path, file_name))
        #     self.images_manager.add_image(image)
        self.input_image_widget.init_box(self.images_manager.images)
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

