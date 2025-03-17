import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QSizePolicy
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt, QPoint, QRect

from tools.load import get_ui_path


class DrawingWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(get_ui_path('picture_cutter.ui'), self)

        self.start = QPoint()
        self.end = QPoint()
        self.rect = None
        self.drawing = False

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start = event.pos()
            self.end = event.pos()
            self.drawing = True

    def mouseMoveEvent(self, event):
        if self.drawing:
            self.end = event.pos()
            # self.update()
            self.paintEvent(None)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.drawing:
            self.end = event.pos()
            self.rect = QRect(self.start, self.end).normalized()
            self.drawing = False
            self.paintEvent(None)
            self.update()

    def paintEvent(self, event):
        qp = QPainter(self)
        print(1)
        if self.rect is not None:
            pen = QPen(Qt.black, 2)
            qp.setPen(pen)
            qp.drawRect(self.rect)

        if self.drawing:
            rect = QRect(self.start, self.end).normalized()
            pen = QPen(Qt.red, 2)
            qp.setPen(pen)
            qp.drawRect(rect)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drag to Draw Rectangle")
        self.setGeometry(100, 100, 800, 600)

        self.widget = DrawingWidget()
        self.setCentralWidget(self.widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())