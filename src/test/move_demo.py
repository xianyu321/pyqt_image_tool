import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout
from PyQt5.QtCore import Qt, QMimeData, QPoint
from PyQt5.QtGui import QDrag


class DraggableButton(QPushButton):
    def __init__(self, row, col, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.startPos = None
        self.row = row
        self.col = col

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.startPos = event.pos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() != Qt.LeftButton or not self.startPos:
            return

        # 创建拖拽对象
        drag = QDrag(self)
        mimeData = QMimeData()

        # 设置mime数据（这里我们仅设置一个空的文本作为示例）
        mimeData.setText("button")
        drag.setMimeData(mimeData)

        # 执行拖放操作
        dropAction = drag.exec_(Qt.MoveAction)

    def mouseReleaseEvent(self, event):
        self.startPos = None
        super().mouseReleaseEvent(event)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.oldPosition = None
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                btn = DraggableButton(i, j, f'{i},{j}')
                btn.setFixedWidth(100)
                row.append(btn)
                grid.addWidget(btn, i, j)
            self.buttons.append(row)

        self.setWindowTitle('Drag and Drop')
        self.show()

    def eventFilter(self, obj, event):
        # 这里处理拖放事件，但由于PyQt的拖放机制，
        # 我们实际上不会在这里直接处理按钮交换。
        # 对于简单的交换逻辑，请参考如何通过鼠标释放位置来计算目标位置并手动交换两个按钮的位置。
        return super().eventFilter(obj, event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())