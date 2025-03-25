from PyQt5.QtGui import QVector3D


# 绘制三角形
def draw_triangle_demo(gl, p1, p2, p3):
    gl.glBegin(gl.GL_TRIANGLES)
    gl.glVertex3d(p1.x(), p1.y(), p1.z())
    gl.glVertex3d(p2.x(), p2.y(), p2.z())
    gl.glVertex3d(p3.x(), p3.y(), p3.z())
    gl.glEnd()

# 绘制正方形
def draw_single_face_demo(p1, p2, p3, p4, gl):
    gl.glBegin(gl.GL_TRIANGLES)
    gl.glVertex3d(p1.x(), p1.y(), p1.z())
    gl.glVertex3d(p2.x(), p2.y(), p2.z())
    gl.glVertex3d(p3.x(), p3.y(), p3.z())
    gl.glEnd()

    gl.glBegin(gl.GL_TRIANGLES)
    gl.glVertex3d(p3.x(), p3.y(), p3.z())
    gl.glVertex3d(p4.x(), p4.y(), p4.z())
    gl.glVertex3d(p1.x(), p1.y(), p1.z())
    gl.glEnd()

# 绘制立方体
def draw_box_faces_demo(gl):
    p1 = QVector3D(-1, -1, -1)
    p2 = QVector3D(+1, -1, -1)
    p3 = QVector3D(+1, +1, -1)
    p4 = QVector3D(-1, +1, -1)
    p5 = QVector3D(-1, -1, 1)
    p6 = QVector3D(+1, -1, 1)
    p7 = QVector3D(+1, +1, 1)
    p8 = QVector3D(-1, +1, 1)

    draw_single_face_demo(p1, p2, p3, p4, gl)
    draw_triangle_demo(p5, p6, p7, p8, gl)

    draw_single_face_demo(p1, p2, p6, p5, gl)
    draw_single_face_demo(p3, p4, p8, p7, gl)

    draw_single_face_demo(p2, p3, p7, p6, gl)
    draw_single_face_demo(p4, p1, p5, p8, gl)

# 绘制一跳线段
def draw_single_line_demo(p1, p2, gl):
    gl.glBegin(gl.GL_LINES)
    gl.glVertex3d(p1.x(), p1.y(), p1.z())
    gl.glVertex3d(p2.x(), p2.y(), p2.z())
    gl.glEnd()


# 绘制正方体轮廓
def draw_box_lines(gl, o = QVector3D(0,0,0)):
    p1 = QVector3D(-1, -1, -1)
    p2 = QVector3D(+1, -1, -1)
    p3 = QVector3D(+1, +1, -1)
    p4 = QVector3D(-1, +1, -1)
    p5 = QVector3D(-1, -1, 1)
    p6 = QVector3D(+1, -1, 1)
    p7 = QVector3D(+1, +1, 1)
    p8 = QVector3D(-1, +1, 1)

    # 一个立方体有12条边
    draw_single_line_demo(p1, p2, gl)
    draw_single_line_demo(p2, p3, gl)
    draw_single_line_demo(p3, p4, gl)
    draw_single_line_demo(p4, p1, gl)

    draw_single_line_demo(p5, p6, gl)
    draw_single_line_demo(p6, p7, gl)
    draw_single_line_demo(p7, p8, gl)
    draw_single_line_demo(p8, p5, gl)

    draw_single_line_demo(p1, p5, gl)
    draw_single_line_demo(p2, p6, gl)
    draw_single_line_demo(p3, p7, gl)
    draw_single_line_demo(p4, p8, gl)
