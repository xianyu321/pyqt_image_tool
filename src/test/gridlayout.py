from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QScrollArea
from PyQt5.QtCore import Qt

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scrollable Grid Layout")
        self.setGeometry(100, 100, 600, 400)

        # 创建一个布局管理器 (QVBoxLayout)，用于容纳 QScrollArea
        main_layout = QVBoxLayout(self)

        # 创建一个 QWidget，用于容纳 QGridLayout
        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)

        # 将 QWidget 放入 QScrollArea
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.grid_widget)  # 设置 grid_widget 为可滚动区域
        self.scroll_area.setWidgetResizable(True)  # 允许内容根据需要调整大小

        # 设置滚动区域为可垂直滚动
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 禁用水平滚动条

        # 将 QScrollArea 添加到主布局中
        main_layout.addWidget(self.scroll_area)

        # 创建按钮用于添加和删除框
        self.add_button = QPushButton("Add Box")
        self.add_button.clicked.connect(self.add_box)

        self.remove_button = QPushButton("Remove Box")
        self.remove_button.clicked.connect(self.remove_box)

        # 创建一个布局来容纳按钮
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.remove_button)

        # 将按钮布局添加到主界面
        main_layout.addLayout(button_layout)

        # 当前子控件的列表
        self.current_boxes = []
        self.box_width = 100  # 固定子框的宽度
        self.box_height = 100  # 固定子框的高度

        # 初始化时根据窗口大小重新排列子控件
        self.rearrange_boxes()

    def add_box(self):
        # 创建一个新的按钮作为子控件
        button = QPushButton("Box")
        button.setFixedSize(self.box_width, self.box_height)  # 固定子框的大小

        # 将子控件添加到布局中
        self.current_boxes.append(button)
        self.rearrange_boxes()

    def remove_box(self):
        if self.current_boxes:
            # 移除最后一个子控件
            last_box = self.current_boxes.pop()
            self.grid_layout.removeWidget(last_box)
            last_box.deleteLater()  # 删除该控件

            # 自动调整布局
            self.rearrange_boxes()

    def rearrange_boxes(self):
        # 获取当前容器的宽度，并计算每行的最大数量
        container_width = self.scroll_area.width()
        max_per_row = max(1, container_width // self.box_width)
        print(max_per_row, container_width)

        # 重新排列子控件
        for i, button in enumerate(self.current_boxes):
            row = i // max_per_row  # 计算行数
            col = i % max_per_row  # 计算列数
            self.grid_layout.addWidget(button, row, col)

    def resizeEvent(self, event):
        # 在窗口大小发生变化时，重新计算并排列子控件
        self.rearrange_boxes()
        event.accept()

app = QApplication([])
window = MyWindow()
window.show()
app.exec_()
