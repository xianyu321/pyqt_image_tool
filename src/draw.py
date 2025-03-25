import os.path

from PyQt5.QtGui import QVector3D

from file import load_texture_from_file
from tools.load import get_texture_dir
from tools.voxel import Voxel

# 绘制三角形
def draw_triangle(gl, triangle, vertices, uvs, o = QVector3D(0,0,0)):
    gl.glBegin(gl.GL_TRIANGLES)
    for index in triangle:
        gl.glTexCoord2f(uvs[index][0], uvs[index][1])
        vox = Voxel.vertices[vertices[index]] + o
        gl.glVertex3f(vox.x(), vox.y(), vox.z())
    gl.glEnd()

# 绘制正方形
def draw_single_face(gl, vertices, uvs, o = QVector3D(0,0,0)):
    for triangle in Voxel.triangle_index:
        draw_triangle(gl, triangle, vertices, uvs, o)

# 绘制立方体
def draw_box_faces(gl, gl_tex, o = QVector3D(0,0,0)):
    vertices_arr, uvs_arr = Voxel.get_all_face()
    gl_tex.bind()
    gl.glEnable(gl.GL_TEXTURE_2D)
    for i in range(len(vertices_arr)):
        vertices = vertices_arr[i]
        uvs = uvs_arr[i]
        draw_single_face(gl, vertices, uvs, o)

def draw_filled_cube(gl):
    # 设置z-buff偏移
    gl.glEnable(gl.GL_POLYGON_OFFSET_FILL)
    gl.glPolygonOffset(1, 1)

    # 绘制填充面
    gl.glColor3f(0.9, 0.83, 0.6)
    draw_box_faces(gl)

    # 关闭z-buff偏移
    gl.glDisable(gl.GL_POLYGON_OFFSET_FILL)

    # 绘制线框
    gl.glColor3f(0.0, 0.0, 0.0)
    # draw_box_lines(gl)

# 绘制一跳线段
def draw_single_line(gl, p1, p2):
    gl.glBegin(gl.GL_LINES)
    gl.glVertex3d(p1.x(), p1.y(), p1.z())
    gl.glVertex3d(p2.x(), p2.y(), p2.z())
    gl.glEnd()

def draw_box_lines(gl, o = QVector3D(0,0,0)):
    for edge in Voxel.edges:
        draw_single_line(gl, Voxel.vertices[edge[0]] + o, Voxel.vertices[edge[1]] + o)


is_built = False
gl_tex = None

def draw(gl):
    global is_built, gl_tex

    if not is_built:
        gl_tex = load_texture_from_file(os.path.join(get_texture_dir(), "amethyst_block.png"))
        is_built = True

    # 设置z-buff偏移
    gl.glEnable(gl.GL_POLYGON_OFFSET_FILL)
    gl.glPolygonOffset(1, 1)
    gl.glColor3f(1,1,1)

    # 绘制填充面
    draw_box_faces(gl, gl_tex)

    # 关闭z-buff偏移
    gl.glDisable(gl.GL_POLYGON_OFFSET_FILL)

    # 绘制线框
    gl.glColor3f(0.0, 0.0, 0.0)
    draw_box_lines(gl)


