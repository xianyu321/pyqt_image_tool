import math
import os

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QImage, QPainter
from PyQt5.QtWidgets import QLabel, QGridLayout, QWidget, QSpacerItem, QSizePolicy

from enity.BlockItem import BlockItem
from enity.Config import JsonConfig, OutputConfig
from manager.BindManager import BindManager
from manager.EventManager import EventManager
from manager.TextureManager import TextureManager
from models.ClickLabel import ClickLabel
from tools.load import get_ui_img_path, get_setting_blocks_path, get_setting_texture_path
from tools.local_save import save_json, load_json
from view.block_widget_item import BlockWidgetItem


class BlocksWidget(QWidget):
    columns = 4 # 总共几列
    icon_size = 64
    def __init__(self):
        super().__init__()
        self.blocks = []
        self.block_widgets = []
        self.box = QGridLayout(self)
        self.setLayout(self.box)
    def init_data(self):
        json_data = self.open_by_json()
        for item in json_data:
            faces = item['faces']
            for face_index in faces.values():
                texture_manager:TextureManager = TextureManager.get_instance()
                texture_manager.add_tex(face_index)

            block = BlockItem(item['name'], faces['left'],faces['right'],faces['front'],faces['back'],faces['up'],faces['down'])
            self.add_block(block)
        if len(self.blocks) > 0:
            e: EventManager = EventManager.get_instance()
            e.emit("update_bind_window", self.blocks[0])
            e.on("update_mini_block", self.block_widgets[0].update_mini_block)
        self.rearrange_boxes()

    def add_block(self, block:BlockItem):
        block_widget = BlockWidgetItem(block_info=block)
        self.blocks.append(block)
        self.block_widgets.append(block_widget)
        self.rearrange_boxes()
    def new_block(self):
        block = BlockItem('block_name')
        self.add_block(block)
    def rearrange_boxes(self):
        spacer = QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.box.addItem(spacer, self.columns, self.columns)
        for i, button in enumerate(self.block_widgets):
            row = i // self.columns  # 计算行数
            col = i % self.columns  # 计算列数
            self.box.addWidget(button, row, col)
        add_img_path = get_ui_img_path("add.png")
        img = QImage(add_img_path)
        add_label = ClickLabel(image=img, cb=self.new_block)
        add_index = len(self.block_widgets)
        self.box.addWidget(add_label, add_index // self.columns, add_index % self.columns)
        QTimer.singleShot(0, self.adjustSize)

    def get_width(self):
        grid_con = BlockWidgetItem.window_size * self.columns + (self.columns - 1) * (self.box.horizontalSpacing())
        grid_width = grid_con + self.box.contentsMargins().left() + self.box.contentsMargins().right()
        return grid_width

    def get_json_dir(self):
        images_path = get_setting_blocks_path()
        json_dir = os.path.join(images_path, JsonConfig.blocks)
        return json_dir
    def save_to_json(self):
        json_data = []
        for item in self.blocks:
            json_data.append({
                'name': item.name,
                'faces': item.faces
            })
        save_json(self.get_json_dir(), json_data)
    def open_by_json(self):
        file_path = self.get_json_dir()
        if not os.path.isfile(file_path):
            self.save_to_json()
        file_json = load_json(file_path)
        return file_json
    def export_json(self):
        file_dir = os.path.join(get_setting_texture_path(), JsonConfig.blocks)
        img_list = list(TextureManager.get_instance().img_map.keys())
        json_data = []
        for i, item in enumerate(self.blocks):
            faces = {}
            for key, value in item.faces.items():
                faces[key] = img_list.index(value)
            json_data.append({
                'name': item.name,
                'faces': faces,
                'icon' : i
            })
        save_json(file_dir, json_data)
        self.export_icon()
    def export_icon(self):
        file_dir = os.path.join(get_setting_texture_path(), "icon.png")
        num_items = len(self.block_widgets)
        packer_size = math.ceil(math.sqrt(num_items))
        size = self.icon_size * packer_size
        icon_img = QImage(size, size, QImage.Format_ARGB32)
        icon_img.fill(0)
        painter = QPainter(icon_img)
        for i,item in enumerate(self.block_widgets):
            img = item.capture_camera_view().scaled(BlocksWidget.icon_size, BlocksWidget.icon_size,
                              aspectRatioMode=Qt.IgnoreAspectRatio,
                              transformMode=Qt.SmoothTransformation)
            rol = i // packer_size  # 计算行数
            col = i % packer_size  # 计算列数
            x, y = self.pixel_address(rol, col)
            painter.drawImage(y, x, img)
        painter.end()
        icon_img.save(file_dir, "PNG")
    def pixel_address(self, rol, col):
        return rol * self.icon_size, col * self.icon_size



