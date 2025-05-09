import sys

from PyQt5.QtCore import (QPoint)
from PyQt5.QtGui import (QMatrix4x4, QVector3D, QOpenGLVersionProfile)
from PyQt5.QtWidgets import QApplication, QOpenGLWidget
from OpenGL.GL import *
from OpenGL.GLU import *
from enity.BlockItem import BlockItem
from manager.EventManager import EventManager
from src.draw import draw, draw_textured_cube


class GLWidget(QOpenGLWidget):
    def __init__(self, parent):
        super().__init__(parent)
        # super(GLWidget, self).__init__(parent)
        self.dragPressPos = QPoint()
        self.rotX = 0
        self.rotZ = 0
        self.ps_button = 0
        self.ps_rotX = 0
        self.ps_rotZ = 0
        self.zoom = 5
        event:EventManager = EventManager.get_instance()
        event.on("update_bind_window", self.set_block)
        self.block:BlockItem = BlockItem('test')

    def set_block(self, block: BlockItem):
        self.block = block
        self.update()
    # --------------------
    # 创建OpenGL环境
    # Qt6 和 Qt5的主要区别在这里
    # --------------------
    def initializeGL(self):
        version_profile = QOpenGLVersionProfile()
        version_profile.setVersion(2, 0)
        # glEnable(GL_DEPTH_TEST)         # 启用深度测试
        self.gl = self.context().versionFunctions(version_profile)
        self.gl.initializeOpenGLFunctions()
        glLineWidth(3)
    def paintEvent(self, event = None):
        # Step 0
        self.makeCurrent()
        # Step 1
        self.gl.glClearColor(0.85, 0.85, 0.85, 1.0)
        self.gl.glClear(self.gl.GL_COLOR_BUFFER_BIT | self.gl.GL_DEPTH_BUFFER_BIT)
        self.gl.glEnable(self.gl.GL_DEPTH_TEST)
        # Step 2
        self.SetupMatrix()
        # Step 3
        self.drawTarget(self.gl)
        # draw(self.gl)
        self.gl.glEnable(GL_TEXTURE_2D)         # 启用纹理映射
        self.gl.glColor3f(1.0, 1.0, 1.0)
        draw_textured_cube(self.block)
        self.gl.glDisable(GL_TEXTURE_2D)
    def drawTarget(self, gl):
        p = QVector3D(0, 0, 0)
        gl.glEnable(GL_COLOR_MATERIAL)
        gl.glColor3f(1.0, 0.0, 0.0)
        gl.glBegin(gl.GL_LINES)
        gl.glVertex3d(p.x() - 5, p.y(), p.z())
        gl.glVertex3d(p.x() + 5, p.y(), p.z())
        gl.glEnd()

        gl.glColor3f(0.0, 1.0, 0.0)
        gl.glBegin(gl.GL_LINES)
        gl.glVertex3d(p.x(), p.y() - 5, p.z())
        gl.glVertex3d(p.x(), p.y() + 5, p.z())
        gl.glEnd()

        gl.glColor3f(0.0, 0.0, 1.0)
        gl.glBegin(gl.GL_LINES)
        gl.glVertex3d(p.x(), p.y(), p.z() - 5)
        gl.glVertex3d(p.x(), p.y(), p.z() + 5)
        gl.glEnd()
        self.gl.glDisable(GL_COLOR_MATERIAL)

    # --------------------
    # 设置矩阵
    # 透视矩阵和Camera矩阵
    # --------------------
    def SetupMatrix(self):
        # ViewPort
        w = self.width()
        h = self.height()
        self.gl.glViewport(0, 0, w, h)

        # Projection
        self.gl.glMatrixMode(self.gl.GL_PROJECTION)
        pm = QMatrix4x4()
        aspectRatio = w / h
        fov = 45 / aspectRatio if w < h else 45
        pm.perspective(fov, w / h, 2, 5000)
        self.gl.glLoadMatrixf(pm.data())

        # Camera
        self.gl.glMatrixMode(self.gl.GL_MODELVIEW)
        self.gl.glLoadIdentity()

        self.gl.glTranslatef(0.0, 0.0, -self.zoom)
        self.gl.glRotatef(self.rotX, 1.0, 0.0, 0.0)
        self.gl.glRotatef(self.rotZ, 0.0, 1.0, 0.0)

    # --------------------
    # 视角控制
    # 1、左键旋转
    # 2、中间缩放
    # --------------------
    def mousePressEvent(self, event):
        self.dragPressPos = event.pos()

        self.ps_button = event.button()
        self.ps_rotX = self.rotX
        self.ps_rotZ = self.rotZ

    def mouseMoveEvent(self, event):
        diff = event.pos() - self.dragPressPos
        if self.ps_button == 1:
            self.rotX = self.ps_rotX + diff.y() * 0.5
            if self.rotX > 90:
                self.rotX = 90
            if self.rotX < -90:
                self.rotX = -90
                # rotZ
            self.rotZ = self.ps_rotZ + diff.x() * 0.5

        self.repaint()

    def wheelEvent(self, event):
        delta = event.angleDelta().y()

        if delta < 0:
            self.zoom += self.zoom * 0.2
        else:
            self.zoom -= self.zoom * 0.2

        self.repaint()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = GLWidget(None)
    widget.resize(640, 480)
    widget.show()
    sys.exit(app.exec())

