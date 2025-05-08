from PyQt5.QtCore import Qt, QMimeData, QByteArray, QBuffer
from PyQt5.QtGui import QDrag, QPixmap, QImage
from PyQt5.QtWidgets import QLabel, QApplication


class MoveLabel(QLabel):
    label_width = 64
    label_height = 64
    label_show_size = 68
    def __init__(self, text = "", parent=None, image:QImage = None, read_olay = False):
        super().__init__(text, parent)
        self.setFixedSize(self.label_show_size, self.label_show_size)
        self.is_selected = False
        self.is_mouse_enter = False
        self.update_style()
        self.setAcceptDrops(True)  # 启用拖放
        self.drag_start_position = None
        self.read_olay = read_olay
        self.index = -1
        if image is not None:
            pix = QPixmap.fromImage(image).scaled(self.label_width, self.label_height, transformMode=Qt.FastTransformation)
            self.setPixmap(pix)
    def set_image_index(self, index):
        self.index = index
    def set_read_olay(self, read_olay = True):
        self.read_olay = read_olay
    def mousePressEvent(self, event):
        self.is_selected = not self.is_selected
        self.update_style()
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return
        drag = QDrag(self)
        mime_data = QMimeData()
        # 将 QPixmap 转换为 PNG 格式的二进制数据
        image = self.pixmap().toImage()
        mime_data.setImageData(image)
        mime_data.setText(self.index.__str__())
        drag.setMimeData(mime_data)
        # 设置拖动时显示的图标
        drag.setPixmap(self.pixmap())
        drag.setHotSpot(event.pos())
        drag.exec_(Qt.CopyAction)

    def dragEnterEvent(self, event):
        if not self.read_olay:
            if event.mimeData().hasImage():
                event.acceptProposedAction()

    def dropEvent(self, event):
        if not self.read_olay:
            if event.mimeData().hasImage():
                image = event.mimeData().imageData()
                self.setPixmap(QPixmap.fromImage(image))
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
