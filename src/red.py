from PyQt5.QtWidgets import QLabel, QApplication, QWidget, QVBoxLayout
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        label = QLabel("这是一个有背景颜色的标签")

        # 设置自动填充背景
        label.setAutoFillBackground(True)

        # 创建一个调色板并设置背景颜色
        palette = label.palette()
        palette.setColor(QPalette.Window, QColor(Qt.red))  # 设置背景颜色为红色
        label.setPalette(palette)

        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())