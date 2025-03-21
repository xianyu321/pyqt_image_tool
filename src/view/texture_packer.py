from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QGridLayout, QApplication, QPushButton

from models.ImageMoveWidget import ImageMoveWidget
from models.MoveLabel import MoveLabel
from tools.load import get_ui_path


class TexturePacker(QWidget):
    texture_box: QGridLayout
    input_image_box: QGridLayout
    block_box: QGridLayout

    input_image_btn: QPushButton
    output_image_btn: QPushButton
    textures = []
    input_images = []
    blocks = []

    def __init__(self):
        super().__init__()
        uic.loadUi(get_ui_path('texture.ui'), self)
        self.box_width = 64  # 固定子框的宽度
        self.box_height = 64  # 固定子框的高度
        self.input_image_btn.clicked.connect(self.add_box)
        # 设置滚动区域为可垂直滚动

    def add_box(self):
        # 创建一个新的按钮作为子控件
        # button = QPushButton("Box")
        # button.setFixedSize(self.box_width, self.box_height)  # 固定子框的大小

        # 将子控件添加到布局中
        # self.input_images.append(button)
        item = MoveLabel('test')
        self.input_images.append(item)
        self.rearrange_boxes()


    def rearrange_boxes(self):
        # 重新排列子控件
        for i, button in enumerate(self.input_images):
            row = i // 5  # 计算行数
            col = i % 5  # 计算列数
            self.input_image_box.addWidget(button, row, col)
        self.input_image_box.parentWidget().adjustSize()


    def onInputImageBtnClicked(self):
        print('input image btn clicked')

if __name__ == '__main__':
    app = QApplication([])
    ex = TexturePacker()
    ex.show()
    app.exec_()

