import os.path

from OpenGL.raw.GL.ARB.tessellation_shader import GL_QUADS
from PyQt5.QtGui import QVector3D, QImage
from OpenGL.GL import *
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


def draw_textured_cube(block):
    """绘制带有纹理的立方体"""
    texture_ids = glGenTextures(6)
    bind_texture(block, texture_ids)
    # 定义立方体的顶点和纹理坐标
    vertices_arr, uvs_arr = Voxel.get_all_face()
    for index, vertices in enumerate(vertices_arr):
        uvs = uvs_arr[index]
        glBindTexture(GL_TEXTURE_2D, texture_ids[index])  # 绑定对应纹理
        glBegin(GL_QUADS)
        for uv_index, vertice_index in enumerate(vertices):
            glTexCoord2fv(uvs[uv_index])
            vertice = Voxel.vertices[vertice_index]
            glVertex3fv([vertice.x(), vertice.y(), vertice.z()])
        glEnd()
def bind_texture(block, texture_ids):
    faces_name_list = list(Voxel.faces.keys())
    for key, img in block.face_textures.items():
        img = img.mirrored()
        index = faces_name_list.index(key)
        if img.isNull():
            print(f"Failed to load texture: {index}")
            continue
        # 将图片转换为 RGBA 格式
        img = img.convertToFormat(QImage.Format_RGBA8888)
        # 绑定纹理
        glBindTexture(GL_TEXTURE_2D, texture_ids[index])
        glTexImage2D(
            GL_TEXTURE_2D, 0, GL_RGBA,
            img.width(), img.height(),
            0, GL_RGBA, GL_UNSIGNED_BYTE, img.bits().asstring(img.byteCount())
        )

        # 设置纹理参数
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)