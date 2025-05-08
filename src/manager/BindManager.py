from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QLineEdit

from enity.BlockItem import BlockItem
from manager.EventManager import EventManager
from manager.ImagesManager import ImagesManager
from manager.TextureManager import TextureManager
from models.BindLabel import BindLabel


class BindManager:
    def __init__(self,name: QLineEdit, left:BindLabel, right:BindLabel, front:BindLabel, back:BindLabel, up:BindLabel, down:BindLabel):
        self.name_text = name
        self.faces = {
            'left' : left,
            'right' : right,
            'front' : front,
            'back' : back,
            'up' : up,
            'down' : down
        }
        self.block:BlockItem = None
        event:EventManager = EventManager.get_instance()
        event.on("update_bind_window", self.set_block)
        event.on("bind_tex", self.set_tex)
        self.name_text.textChanged.connect(self.on_text_changed)

    def on_text_changed(self):
        text = self.name_text.text()
        self.block.name = text
    def set_block(self, block:BlockItem):
        self.block = block
        self.update_tex()
    def update_tex(self):
        if self.block is not None:
            self.name_text.setText(self.block.name)
            for key, img in self.block.face_textures.items():
                self.faces[key].set_image(img)
    def set_tex(self, label:BindLabel, index:int):
        tex = ImagesManager.get_instance().get_q_image(index)
        face_name = label.objectName()
        if label.image == BlockItem.text_img:
            TextureManager.get_instance().reduce_txe(self.block.faces[face_name])
        TextureManager.get_instance().add_tex(index)
        self.block.face_textures[face_name] = tex
        self.block.faces[face_name] = index
        event:EventManager = EventManager.get_instance()
        event.emit("update_bind_window", self.block)


