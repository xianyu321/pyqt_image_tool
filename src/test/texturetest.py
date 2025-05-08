from PyQt5.QtGui import QImage, QPainter
from PyQt5.QtCore import QRect

def combine_qimages_to_png(qimage_list, output_path, spacing=10):
    """
    将多个 QImage 合并为一个 PNG 图像并保存。

    :param qimage_list: 包含多个 QImage 的列表
    :param output_path: 输出的 PNG 文件路径
    :param spacing: 每个图像之间的间距（像素）
    """
    if not qimage_list:
        raise ValueError("qimage_list 不能为空")

    # 获取所有 QImage 的宽度和高度
    max_width = max(img.width() for img in qimage_list)
    total_height = sum(img.height() for img in qimage_list) + spacing * (len(qimage_list) - 1)

    # 创建一个新的 QImage 作为画布
    combined_image = QImage(max_width, total_height, QImage.Format_ARGB32)
    combined_image.fill(0xFFFFFFFF)  # 填充白色背景

    # 使用 QPainter 进行绘制
    painter = QPainter(combined_image)
    y_offset = 0
    for img in qimage_list:
        painter.drawImage(QRect(0, y_offset, img.width(), img.height()), img)
        y_offset += img.height() + spacing
    painter.end()

    # 保存为 PNG 文件
    if not combined_image.save(output_path, "PNG"):
        raise RuntimeError(f"无法保存图像到 {output_path}")

# 示例用法
if __name__ == "__main__":
    # 创建一些示例 QImage
    image1 = QImage(100, 50, QImage.Format_ARGB32)
    image1.fill(0xFFFF0000)  # 红色
    image2 = QImage(100, 50, QImage.Format_ARGB32)
    image2.fill(0xFF00FF00)  # 绿色
    image3 = QImage(100, 50, QImage.Format_ARGB32)
    image3.fill(0xFF0000FF)  # 蓝色

    # 合并并保存
    combine_qimages_to_png([image1, image2, image3], "combined.png", spacing=10)