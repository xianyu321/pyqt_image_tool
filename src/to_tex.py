import sys
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtGui import QImage, QPixmap, QPainter, QTransform, QDragEnterEvent, QDropEvent
from PyQt5.QtCore import Qt, QMimeData, QSize


class PixelatedLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.scaled_image = None

    def set_scaled_image(self, image):
        self.scaled_image = image
        self.update()

    def paintEvent(self, event):
        if self.scaled_image is not None:
            painter = QPainter(self)
            pixmap = QPixmap.fromImage(self.scaled_image)

            # 计算适应窗口大小的新尺寸
            scaled_pixmap = pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.FastTransformation)

            # 手动绘制缩放后的图像
            painter.drawPixmap(self.rect(), scaled_pixmap)
            painter.end()
        else:
            super().paintEvent(event)


class ImageResizerWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("拖拽调整图像大小")
        self.setGeometry(300, 300, 600, 600)

        self.layout = QVBoxLayout()
        self.label = PixelatedLabel(self)  # 使用自定义的 PixelatedLabel

        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        # 启用拖放功能
        self.setAcceptDrops(True)

        # 初始化图像变量
        self.scaled_image = None

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            self.resize_image(file_path)

    def resize_image(self, image_path):
        max_width, max_height = 16, 16  # 设定最大宽度和高度

        image = QImage(image_path)
        if image.isNull():
            QMessageBox.critical(self, "错误", f"无法加载图像: {image_path}")
            return

        original_width = image.width()
        original_height = image.height()

        # 计算新的尺寸
        ratio = min(max_width / original_width, max_height / original_height)
        new_width = int(original_width * ratio)
        new_height = int(original_height * ratio)

        # 调整图像大小并保持比例，使用最近邻插值
        self.scaled_image = image.scaled(new_width, new_height,
                                         aspectRatioMode=Qt.KeepAspectRatio,
                                         transformMode=Qt.SmoothTransformation)  # 使用最近邻插值

        self.label.set_scaled_image(self.scaled_image)

    def resizeEvent(self, event):
        # 在窗口大小改变时更新图像显示
        if self.scaled_image is not None:
            self.label.set_scaled_image(self.scaled_image)
        super().resizeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageResizerWidget()
    window.show()
    sys.exit(app.exec_())