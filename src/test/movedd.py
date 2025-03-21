import sys

from PyQt5.QtGui import QDrag
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QScrollArea, QVBoxLayout
from PyQt5.QtCore import Qt, QPoint, QMimeData


class DraggableButton(QPushButton):
    def __init__(self, row, col, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.startPos = None
        self.originalPosition = None
        self.row = row
        self.col = col

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.startPos = event.pos()
            self.originalPosition = (self.row, self.col)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        if not self.startPos:
            return

        drag = QDrag(self)
        mimeData = QMimeData()
        mimeData.setText(f"{self.row},{self.col}")
        drag.setMimeData(mimeData)

        dropAction = drag.exec_(Qt.MoveAction)

        if dropAction == Qt.MoveAction and hasattr(self.parent(), 'swapCells'):
            targetRow, targetCol = self.parent().lastTarget
            self.parent().swapCells(self.originalPosition[0], self.originalPosition[1], targetRow, targetCol)


class DragLayoutWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.lastTarget = None

    def addButtons(self):
        for i in range(3):
            for j in range(3):
                btn = DraggableButton(i, j, f'{i},{j}')
                self.layout.addWidget(btn, i, j)

    def swapCells(self, fromRow, fromCol, toRow, toCol):
        widgetFrom = self.layout.itemAtPosition(fromRow, fromCol).widget()
        widgetTo = self.layout.itemAtPosition(toRow, toCol).widget()

        self.layout.removeWidget(widgetFrom)
        self.layout.removeWidget(widgetTo)

        self.layout.addWidget(widgetTo, fromRow, fromCol)
        self.layout.addWidget(widgetFrom, toRow, toCol)

        widgetFrom.row, widgetFrom.col = toRow, toCol
        widgetTo.row, widgetTo.col = fromRow, fromCol


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        scroll = QScrollArea()
        widget = DragLayoutWidget()
        widget.addButtons()
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)

        layout = QVBoxLayout(self)
        layout.addWidget(scroll)
        self.setLayout(layout)

        self.setWindowTitle('Drag and Drop GridLayout')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())