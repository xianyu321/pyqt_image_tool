import os
import sys
from PyQt5.QtWidgets import QApplication, QOpenGLWidget
from PyQt5.QtGui import QImage
from OpenGL.GL import *
from OpenGL.GLU import *

from tools import voxel
from tools.load import get_texture_dir
from tools.voxel import Voxel


class TexturedCube(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.texture_ids = []  # 存储纹理 ID
        self.setFixedSize(64, 64)

    def initializeGL(self):
        """初始化 OpenGL 环境"""
        glClearColor(0.2, 0.2, 0.2, 1)  # 设置背景颜色
        glEnable(GL_DEPTH_TEST)         # 启用深度测试
        glEnable(GL_TEXTURE_2D)         # 启用纹理映射
        self.load_textures()            # 加载纹理

    def load_textures(self):
        """加载纹理"""
        texture_files = [
            os.path.join(get_texture_dir(), "amethyst_block.png"),  # 前面
            os.path.join(get_texture_dir(), "amethyst_block.png"),  # 后面
            os.path.join(get_texture_dir(), "amethyst_block.png"),  # 左面
            os.path.join(get_texture_dir(), "amethyst_block.png"),  # 右面
            os.path.join(get_texture_dir(), "amethyst_block.png"),  # 底面
            os.path.join(get_texture_dir(), "amethyst_block.png")  # 顶面
        ]

        # 生成纹理 ID
        self.texture_ids = glGenTextures(len(texture_files))

        for i, texture_file in enumerate(texture_files):
            image = QImage(texture_file).mirrored()  # 使用 QImage 加载图片（镜像翻转以匹配 OpenGL 坐标系）
            if image.isNull():
                print(f"Failed to load texture: {texture_file}")
                continue

            # 将图片转换为 RGBA 格式
            image = image.convertToFormat(QImage.Format_RGBA8888)

            # 绑定纹理
            glBindTexture(GL_TEXTURE_2D, self.texture_ids[i])
            glTexImage2D(
                GL_TEXTURE_2D, 0, GL_RGBA,
                image.width(), image.height(),
                0, GL_RGBA, GL_UNSIGNED_BYTE, image.bits().asstring(image.byteCount())
            )

            # 设置纹理参数
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    def paintGL(self):
        """绘制场景"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # 设置视角
        gluPerspective(45, self.width() / self.height(), 0.1, 100.0)

        # 移动相机位置并旋转视角
        glTranslatef(0, 0, -2.5)  # 移动相机远离立方体，使其可见
        glRotatef(45, 1, 0, 0)  # 绕X轴旋转45
        glRotatef(45, 0, 1, 0)  # 绕y轴旋转45

        self.draw_textured_cube()

    def resizeGL(self, width, height):
        """调整窗口大小时更新视口"""
        glViewport(0, 0, width, height)

    def draw_textured_cube(self):
        """绘制带有纹理的立方体"""
        # 定义立方体的顶点和纹理坐标
        vertices_arr, uvs_arr = Voxel.get_all_face()
        for index, vertices in enumerate(vertices_arr):
            uvs = uvs_arr[index]
            glBindTexture(GL_TEXTURE_2D, self.texture_ids[index])  # 绑定对应纹理
            glBegin(GL_QUADS)
            for uv_index, vertice_index in enumerate(vertices):
                glTexCoord2fv(uvs[uv_index])
                vertice = Voxel.vertices[vertice_index]
                glVertex3fv([vertice.x(), vertice.y(), vertice.z()])
            glEnd()
# 主程序
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TexturedCube()
    window.setWindowTitle("Textured Cube with PyQt5 and OpenGL")
    window.resize(64, 64)
    window.show()
    sys.exit(app.exec_())