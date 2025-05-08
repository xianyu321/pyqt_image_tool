import os
import sys

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QApplication, QOpenGLWidget
from PyQt5.QtGui import QImage, QPainter, QSurfaceFormat
from OpenGL.GL import *
from OpenGL.GLU import *

from draw import draw_textured_cube
from enity.BlockItem import BlockItem
from manager.EventManager import EventManager
from tools.voxel import Voxel


class BlockWidgetItem(QOpenGLWidget):
    window_size = 100
    def __init__(self,block_info:BlockItem, parent=None):
        super().__init__(parent)
        self.block_info = block_info
        self.texture_ids = []  # 存储纹理 ID
        self.setFixedSize(self.window_size, self.window_size)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
    def sizeHint(self):
        return QSize(self.window_size, self.window_size)
    def minimumSizeHint(self):
        return QSize(self.window_size, self.window_size)
    def initializeGL(self):
        """初始化 OpenGL 环境"""
        glClearColor(0.0, 0.0, 0.0, 0)  # 设置背景颜色
        glEnable(GL_DEPTH_TEST)         # 启用深度测试
        glEnable(GL_TEXTURE_2D)         # 启用纹理映射
        glEnable(GL_BLEND)  # 启用混合模式
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # 设置透明混合模式

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            e: EventManager = EventManager.get_instance()
            e.emit("update_bind_window", self.block_info)
            e.off("update_mini_block")
            e.on("update_mini_block", self.update_mini_block)
    def update_mini_block(self):
        self.update()
        # self.paintGL()
    def paintGL(self):
        """绘制场景"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # 设置视角
        gluPerspective(45, self.width() / self.height(), 0.1, 100.0)

        # 移动相机位置并旋转视角
        glTranslatef(0, 0, -2.2)  # 移动相机远离立方体，使其可见
        glRotatef(45, 1, 0, 0)  # 绕X轴旋转45
        glRotatef(45, 0, 1, 0)  # 绕y轴旋转45

        draw_textured_cube(self.block_info)
        # self.draw_textured_cube()

    def resizeGL(self, width, height):
        """调整窗口大小时更新视口"""
        glViewport(0, 0, width, height)
    def capture_camera_view(self):
        """捕获当前摄像机视角的渲染内容"""
        # 获取当前视口大小
        size = self.size()
        # 创建 QImage 用于存储捕获的图像
        image = QImage(size, QImage.Format_ARGB32)
        image.fill(0)  # 填充背景为透明
        # 使用 QPainter 将 OpenGL 渲染内容绘制到 QImage
        painter = QPainter(image)
        self.render(painter)
        painter.end()
        return image