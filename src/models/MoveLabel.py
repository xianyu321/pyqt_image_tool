from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag
from PyQt5.QtWidgets import QLabel, QApplication


class MoveLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedSize(64, 64)  # 固定按钮的大小
        self.setStyleSheet("background-color: lightgray;")
        self.setAcceptDrops(True)  # 启用拖放

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return

        drag = QDrag(self)
        mime_data = QMimeData()

        # 将按钮的文本作为数据
        mime_data.setText(self.text())

        drag.setMimeData(mime_data)
        drag.setPixmap(self.grab())  # 设置拖动时显示的图像
        drag.setHotSpot(event.pos())

        drag.exec_(Qt.CopyAction | Qt.MoveAction)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasText():
            self.setText(event.mimeData().text())  # 设置拖入目标的文本
            event.acceptProposedAction()