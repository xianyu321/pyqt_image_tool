from PyQt5.QtGui import QImage, QOpenGLTexture


def load_texture_from_file(filepath):
    with open(filepath, 'rb') as hf:
        data = hf.read()

    image = QImage()
    valid = image.loadFromData(data)
    if not valid:
        return False

    gl_tex_obj = QOpenGLTexture(image.mirrored())
    # 取消图片线性插值
    gl_tex_obj.setMinificationFilter(QOpenGLTexture.Nearest)  # 缩小过滤器
    gl_tex_obj.setMagnificationFilter(QOpenGLTexture.Nearest)  # 放大过滤器
    return gl_tex_obj