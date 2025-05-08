import os
from time import sleep

from PyQt5.QtGui import QImage, QSurfaceFormat
from PyQt5.QtWidgets import QWidget, QGridLayout, QApplication, QPushButton, QVBoxLayout, QGroupBox, QScrollArea
from PyQt5.uic import loadUi

from manager.BindManager import BindManager
from manager.EventManager import EventManager
from manager.ImagesManager import ImagesManager
from manager.TextureManager import TextureManager
from models.BlocksWidget import BlocksWidget
from tools.Debug import Debug
# from view.block_item import ToolBar3D
from view.main_widget import GLWidget
from models.ImageMoveWidget import ImageMoveWidget
from tools.load import get_ui_path, get_texture_dir

class TexturePacker(QWidget):
    def __init__(self):
        super().__init__()
        self.images_manager:ImagesManager = ImagesManager.get_instance()
        self.texture_manager:TextureManager = TextureManager.get_instance()
        self.blocks = []

        loadUi(get_ui_path('texture.ui'), self)
        self.bind_manager = BindManager(self.name, self.left,self.right, self.front, self.back,self.up,self.down)
        self.setGeometry(100, 100, 2400, 1200)
        self.groupBox_2:QGroupBox = self.findChild(QGroupBox, "groupBox_2")
        self.groupBox_3:QGroupBox = self.findChild(QGroupBox, "groupBox_3")

        # 网格布局模式
        self.input_image_widget:ImageMoveWidget = self.findChild(ImageMoveWidget, "input_image_widget")
        self.texture_widget: ImageMoveWidget = self.findChild(ImageMoveWidget, "texture_widget")
        self.blocks_widget: BlocksWidget = self.findChild(BlocksWidget, "blocks_widget")

        # 滚动框
        self.scroll_input: QScrollArea = self.findChild(QScrollArea, "scroll_input")
        self.scroll_texture: QScrollArea = self.findChild(QScrollArea, "scroll_texture")
        self.scroll_blocks: QScrollArea = self.findChild(QScrollArea, "scroll_blocks")

        self.input_image_btn : QPushButton =  self.findChild(QPushButton, "input_image_btn")
        self.output_image_btn : QPushButton = self.findChild(QPushButton, "output_image_btn")

        self.input_image_btn.clicked.connect(self.save_clicked)
        self.output_image_btn.clicked.connect(self.export_clicked)
        self.gl_widget = GLWidget(self.main_widget)
        layout = QVBoxLayout(self.main_widget)
        layout.addWidget(self.gl_widget)
    def init_move_widget(self):
        self.input_image_widget.set_read_olay()
        self.input_image_widget.set_read_file()
        self.input_image_widget.set_images_manager(self.images_manager)
        # self.input_image_widget.set_has_add_label()
        self.images_manager.set_widget(self.input_image_widget)
        self.texture_widget.set_read_olay()
    def init_width(self):
        # 添加方框线的宽度
        left_width = self.input_image_widget.get_width() + self.groupBox_2.contentsMargins().left() + self.groupBox_2.contentsMargins().right()
        self.scroll_input.setFixedWidth(left_width)
        self.scroll_texture.setFixedWidth(left_width)
        right_width = self.blocks_widget.get_width() + self.groupBox_3.contentsMargins().left() + self.groupBox_3.contentsMargins().right()
        self.blocks_widget.setFixedWidth(right_width)
        self.scroll_blocks.setFixedWidth(right_width + 10)

    def show(self):
        super().show()
        self.init_move_widget()
        self.init_width()
        self.init_data()

    def init_data(self):
        self.images_manager.init_image_by_json()
        self.input_image_widget.init_box(self.images_manager.images)
        self.blocks_widget.init_data()
        e:EventManager = EventManager.get_instance()
        e.on("update_texture", self.update_texture)
        e.emit("update_texture")
        return
    def update_texture(self):
        self.texture_widget.init_box(self.texture_manager.get_all_tex())

    def showEvent(self, event):
        super().showEvent(event)

    def add_box(self):
        return
    def save_clicked(self):
        Debug.Log('save_clicked')
        self.blocks_widget.save_to_json()
    def export_clicked(self):
        Debug.Log('export_clicked')
        self.blocks_widget.save_to_json()
        self.texture_manager.export_all()
        self.blocks_widget.export_json()

if __name__ == '__main__':
    app = QApplication([])


    ex = TexturePacker()
    ex.show()
    app.exec_()

