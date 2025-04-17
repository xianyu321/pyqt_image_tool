import os

from PyQt5.QtGui import QImage, QOpenGLTexture

from tools.load import get_texture_dir


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

# print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# filepath = os.path.join(get_texture_dir(), "amethyst_block.png")
# print(os.path.join(get_texture_dir(), "amethyst_block.png"))
# filepath = r"D:\project\python\pyqt_image_tool\static\texture\amethyst_block.png"
# if os.path.exists(filepath):
#     print("File exists and accessible.")
# else:
#     print("File does not exist or is not accessible.")
# with open(filepath, 'rb') as hf:
#     data = hf.read()