from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QGridLayout, QSpacerItem, QSizePolicy, QLabel

from enity.ImageItem import ImageItem
from models.MoveLabel import MoveLabel
from tools.load import get_ui_img_path


class ImageMoveWidget(QWidget):
    columns = 8 # 总共几列
    def __init__(self, images_manager = None, read_olay=False, has_add_label = False, read_file = False):
        super().__init__()
        self.setAcceptDrops(True)  # 允许拖拽
        self.box = QGridLayout(self)
        self.setLayout(self.box)
        self.move_labels = []  # 保存所有的标签
        self.read_olay = read_olay
        self.has_add_label = has_add_label
        self.read_file = read_file
        self.images_manager = images_manager
    def set_images_manager(self, images_manager):
        self.images_manager = images_manager
    def set_read_olay(self, read_olay = True):
        self.read_olay = read_olay
    def set_has_add_label(self, has_add_label = True):
        self.has_add_label = has_add_label
        self.rearrange_boxes()
    def set_read_file(self, read_file = True):
        self.read_file = read_file
    def dropEvent(self, event):
        # 判断打开文件读入模式
        if self.read_file:
            if event.mimeData().hasUrls():
                file_paths = [url.toLocalFile() for url in event.mimeData().urls()]
                if not file_paths:
                    return
                for file_path in file_paths:
                    self.images_manager.add_image_by_copy(file_path)
                event.acceptProposedAction()
        # 判断app内图片拖入模式
        if not self.read_olay:
            if event.mimeData().hasImage():
                print('-----------------')
                label = MoveLabel(image=event.mimeData().imageData())
                self.add_item(len(self.move_labels), label)
                event.acceptProposedAction()

    def dragEnterEvent(self, event):
        # 判断打开文件读入模式
        if self.read_file:
            if event.mimeData().hasUrls():
                event.acceptProposedAction()
        # 判断app内图片拖入模式
        if not self.read_olay:
            if event.mimeData().hasImage():
                event.acceptProposedAction()

    def add_item(self,index:int, label:MoveLabel):

        label.read_olay = self.read_olay
        self.move_labels.insert(index, label)
        # self.move_labels.append(label)
        self.rearrange_boxes()
    def rearrange_boxes(self):
        # while self.box.count():
        #     item = self.box.takeAt(0)  # 获取第一个项
        #     if item.widget():  # 如果是小部件
        #         widget = item.widget()
        #         widget.deleteLater()  # 删除小部件
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
        # self.adjustSize()
        # QTimer.singleShot(0, self.adjustSize)
    def init_box(self, images: []):
        self.move_labels.clear()
        while self.box.count():
            item = self.box.takeAt(0)  # 获取第一个项
            if item.widget():  # 如果是小部件
                widget = item.widget()
                widget.deleteLater()  # 删除小部件
        for index, item in enumerate(images):
            if isinstance(item, QImage):
                move_label = MoveLabel(image=item, read_olay=self.read_olay)
                move_label.set_image_index(index)
                self.move_labels.append(move_label)
            elif isinstance(item, ImageItem):
                move_label = MoveLabel(image=item.image, read_olay=self.read_olay)
                move_label.set_image_index(index)
                self.move_labels.append(move_label)
        self.rearrange_boxes()

    def get_width(self):
        grid_con = MoveLabel.label_show_size * self.columns + (self.columns - 1) * (self.box.horizontalSpacing())
        grid_width = grid_con + self.box.contentsMargins().left() + self.box.contentsMargins().right()
        return grid_width