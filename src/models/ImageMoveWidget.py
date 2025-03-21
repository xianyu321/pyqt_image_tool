import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QScrollArea
from PyQt5.QtCore import Qt, QPoint

class ImageMoveWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)  # 允许拖拽
        # self.grid_layout = QGridLayout(self)
        # self.buttons = []  # 存储按钮
        #
        # # 添加按钮
        # for i in range(3):
        #     btn = QPushButton(f'Button {i + 1}', self)
        #     self.grid_layout.addWidget(btn, i // 2, i % 2)  # 添加到网格
        #     self.buttons.append(btn)

    def mousePressEvent(self, event):
        print(f"Mouse Pressed at {event.pos()}")

    def mouseMoveEvent(self, event):
        print(f"Mouse Moved at {event.pos()}")

    def dropEvent(self, event):
        print(f"Item Dropped at {event.pos()}")
    def dragEnterEvent(self, event):
        print(f"Item dragEnterEvent at {event.pos()}")
        print(self.size())

    def dropMoveEvent(self, event):
        print(f"Item dropMoveEvent at {event.pos()}")


# 运行窗口
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageMoveWidget()
    window.show()
    sys.exit(app.exec_())
