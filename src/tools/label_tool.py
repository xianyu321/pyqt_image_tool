from PyQt5.QtCore import QPoint, QRect
from PyQt5.QtGui import QPixmap, QImage, QPaintDevice
from PyQt5.QtWidgets import QLabel, QWidget

"""
根据label上的点坐标和label及pixmap的尺寸，计算出对应的pixmap上的坐标。

:param label: 显示pixmap的QLabel对象
:param label_x: 点在label上的x坐标
:param label_y: 点在label上的y坐标
:return: 返回一个包含(x, y)坐标的tuple，表示该点在原始pixmap上的位置
"""
def getPixmapPoint(label, point):
    # 获取label和pixmap的尺寸
    label_width = label.width()
    label_height = label.height()
    pixmap = label.pixmap()
    if pixmap is None:
        return None  # 如果没有设置pixmap，则返回None
    pixmap_width = pixmap.width()
    pixmap_height = pixmap.height()

    # 计算缩放比例，选择最小的比例以保持宽高比
    scale_factor = min(label_width / pixmap_width, label_height / pixmap_height)

    # 计算水平和垂直方向上的位移
    horizontal_shift = (label_width - pixmap_width * scale_factor) / 2 if label_width > pixmap_width * scale_factor else 0
    vertical_shift = (label_height - pixmap_height * scale_factor) / 2 if label_height > pixmap_height * scale_factor else 0

    # 转换label上的点到pixmap上的点
    pixmap_x = (point.x() - horizontal_shift) / scale_factor
    pixmap_y = (point.y() - vertical_shift) / scale_factor

    return QPoint(pixmap_x, pixmap_y)

# 示例用法
# 假设你有一个QLabel对象叫做my_label，并且它已经设置了pixmap
# point_on_pixmap = getPixmapPoint(my_label, 100, 150)
# print(f"Point on Pixmap: ({point_on_pixmap[0]}, {point_on_pixmap[1]})")

def adjust_position(original_img, target_img, original_pos, alignment='top-left'):
    """
    根据两张图像的尺寸调整位置

    :param original_size: tuple, 原始图像的尺寸(width, height)
    :param target_size: tuple, 目标图像的尺寸(width, height)
    :param original_pos: tuple, 在原始图像中的位置(x, y)
    :param alignment: str, 对齐方式，默认为'center'
    :return: tuple, 调整后的新位置(new_x, new_y)
    """
    original_width, original_height = original_img.size().width(), original_img.size().height()
    target_width, target_height = target_img.size().width(), target_img.size().height()
    x, y = original_pos.x(), original_pos.y()

    # 计算缩放比例
    scale_width = target_width / original_width
    scale_height = target_height / original_height
    # 根据缩放比例调整原始位置
    new_x = original_pos.x() * scale_width
    new_y = original_pos.y() * scale_height

    if alignment == 'center':
        # 如果需要居中对齐，则进一步调整位置
        center_offset_x = (target_width - original_width * scale_width) / 2
        center_offset_y = (target_height - original_height * scale_height) / 2
        new_x += center_offset_x
        new_y += center_offset_y
    elif alignment == 'top-left':
        # 若是左上角对齐，则不需要额外调整
        pass
    elif alignment == 'bottom-right':
        # 若是右下角对齐，则需要进行相应偏移
        bottom_right_offset_x = target_width - original_width * scale_width
        bottom_right_offset_y = target_height - original_height * scale_height
        new_x += bottom_right_offset_x
        new_y += bottom_right_offset_y
    else:
        raise ValueError("不支持的对齐方式")

    return QPoint(new_x, new_y)


# # 示例使用
# original_size = (800, 600)  # 原始图像尺寸
# target_size = (1600, 1200)  # 目标图像尺寸
# original_pos = (400, 300)  # 原始位置
# new_pos = adjust_position(original_size, target_size, original_pos)
# print(f"调整后的新位置: {new_pos}")


def rect_overflow_clear(rect: QRect, pixmap):
    if rect.left() < 0:
        rect.setLeft(0)
    if rect.right() >= pixmap.width():
        rect.setRight(pixmap.width() - 1)
    if rect.top() < 0:
        rect.setTop(0)
    if rect.bottom() > pixmap.height():
        rect.setBottom(pixmap.height() - 1)