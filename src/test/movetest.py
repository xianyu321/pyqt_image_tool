import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QVBoxLayout, QMainWindow
from PyQt5.QtCore import Qt, QMimeData, QPoint
from PyQt5.QtGui import QDrag

class DraggableButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedSize(100, 50)  # 固定按钮的大小
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


class DragAndDropGridLayout(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Drag and Drop Buttons in GridLayout")
        self.setGeometry(100, 100, 400, 300)

        # 创建布局
        self.grid_layout = QGridLayout(self)
        self.buttons = []

        # 创建一些按钮并将其添加到布局中
        for i in range(4):
            for j in range(3):
                button = DraggableButton(f"Button {i * 3 + j + 1}")
                self.buttons.append(button)
                self.grid_layout.addWidget(button, i, j)

        self.setLayout(self.grid_layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DragAndDropGridLayout()
    window.show()
    sys.exit(app.exec_())
