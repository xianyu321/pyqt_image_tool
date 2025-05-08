from PyQt5.QtCore import Qt, QMimeData, QByteArray, QBuffer
from PyQt5.QtGui import QDrag, QPixmap, QImage
from PyQt5.QtWidgets import QLabel, QApplication

from manager.EventManager import EventManager
from manager.ImagesManager import ImagesManager


class BindLabel(QLabel):
    label_width = 128
    label_height = 128
    label_show_size = 132
    def __init__(self, parent = None, image: QImage = None):
        super().__init__(parent)
        self.setFixedSize(self.label_show_size, self.label_show_size)
        self.is_selected = False
        self.is_mouse_enter = False
        self.update_style()
        self.setAcceptDrops(True)  # 启用拖放
        self.image = image
        self.set_image(image)
    def set_image(self, image = None):
        self.image = image
        if image is not None:
            pix = QPixmap.fromImage(image).scaled(self.label_width, self.label_height, transformMode=Qt.FastTransformation)
            self.setPixmap(pix)
        else:
            self.setPixmap(QPixmap())
    def dragEnterEvent(self, event):
        if self.image is None:
            return
        if event.mimeData().hasImage():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if self.image is None:
            return
        if event.mimeData().hasText():
            index = int(event.mimeData().text())
            images_manager:ImagesManager = ImagesManager.get_instance()
            image = images_manager.get_q_image(index)
            self.set_image(image)
            e = EventManager.get_instance()
            e.emit("bind_tex", self, index)
            e.emit("update_mini_block")
            event.acceptProposedAction()
    def enterEvent(self, event):
        # 鼠标进入时给 QLabel 添加外框
        self.is_mouse_enter = True
        self.update_style()
    def leaveEvent(self, event):
        # 鼠标离开时移除外框
        self.is_mouse_enter = False
        self.update_style()
    def update_style(self):
        if self.is_selected:
            self.setStyleSheet("background-color: lightgray; border: 2px solid #333333;")
        else:
            if self.is_mouse_enter:
                self.setStyleSheet("background-color: lightgray; border: 2px solid #666666;")
            else:
                self.setStyleSheet("background-color: lightgray; border: 2px solid #999999;")
