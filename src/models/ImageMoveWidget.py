from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QGridLayout, QSpacerItem, QSizePolicy, QLabel

from enity.ImageItem import ImageItem
from models.MoveLabel import MoveLabel
from tools.load import get_ui_img_path


class ImageMoveWidget(QWidget):
    columns = 6 # 总共几列
    def __init__(self, read_olay=False, has_add_label = True):
        super().__init__()
        self.setAcceptDrops(True)  # 允许拖拽
        self.box = QGridLayout(self)
        self.setLayout(self.box)
        self.move_labels = []  # 保存所有的标签
        self.reda_olay = read_olay
        self.has_add_label = has_add_label

    def set_read_olay(self, read_olay = False):
        self.reda_olay = read_olay
    def set_has_add_label(self, has_add_label = True):
        self.has_add_label = has_add_label
    def dropEvent(self, event):
        if self.reda_olay:
            return
        if event.mimeData().hasImage():
            label = MoveLabel(image= event.mimeData().imageData())
            self.add_item(len(self.move_labels), label)
            event.acceptProposedAction()
    def dragEnterEvent(self, event):
        if self.reda_olay:
            return
        if event.mimeData().hasImage():
            event.acceptProposedAction()
    def add_item(self,index:int, label:MoveLabel):
        # self.move_labels.insert(index, label)
        self.move_labels.append(label)
        self.rearrange_boxes()
    def rearrange_boxes(self):
        # 重新排列子控件
        # for i in range(self.box.count()):  # 遍历布局中的每个项
        #     item = self.box.itemAt(i)
        #     if item is not None:  # 如果 item 不为 None
        #         widget = item.widget()
        #         if widget:
        #             widget.setParent(None)  # 移除 widget
        spacer = QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.box.addItem(spacer, self.columns, self.columns)

        for i, button in enumerate(self.move_labels):
            row = i // self.columns  # 计算行数
            col = i % self.columns  # 计算列数
            self.box.addWidget(button, row, col)
        if self.has_add_label:
            add_img_path = get_ui_img_path("add.png")
            add_pixmap = QPixmap(add_img_path)
            add_label = QLabel()
            add_label.setPixmap(add_pixmap)
            add_index = len(self.move_labels)
            self.box.addWidget(add_label, add_index // self.columns, add_index % self.columns)

        self.adjustSize()

    def init_box(self, images: []):
        for item in images:
            move_label = None
            if isinstance(item, QImage):
                move_label = MoveLabel(image=item)
                self.move_labels.append(move_label)
            elif isinstance(item, ImageItem):
                move_label = MoveLabel(image=item.image)
                self.move_labels.append(move_label)
            print(item)
            self.move_labels.append(move_label)
        self.rearrange_boxes()

    def getwidth(self):
        grid_con = MoveLabel.label_show_size * self.columns + (self.columns - 1) * (self.box.horizontalSpacing())
        grid_width = grid_con + self.box.contentsMargins().left() + self.box.contentsMargins().right()
        return grid_width