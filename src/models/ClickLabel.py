from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QLabel


class ClickLabel(QLabel):
    label_size = 100
    label_show_size = 100
    def __init__(self, parent=None, image: QImage = None, cb = None):
        super().__init__(parent)
        self.setFixedSize(self.label_show_size, self.label_show_size)
        self.setStyleSheet("background-color: #DDDDDD;")
        self.cb = cb
        if image is not None:
            pix = QPixmap.fromImage(image).scaled(self.label_size, self.label_size,
                                                  transformMode=Qt.FastTransformation)
            self.setPixmap(pix)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.cb is not None:
                self.cb()