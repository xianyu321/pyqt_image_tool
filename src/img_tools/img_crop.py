import sys
from PyQt5.QtWidgets import (QApplication, QLabel, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QFileDialog, QMessageBox)
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QPalette, QColor
from PyQt5.QtCore import Qt, QPoint, QRect, QSize


class ImageCropper(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("图像裁剪器")
        self.setGeometry(300, 300, 1200, 600)
        self.setMouseTracking(True)
        # 主布局
        self.main_layout = QHBoxLayout()

        # 左侧布局：用于选择和显示原图
        self.left_layout = QVBoxLayout()
        self.original_label = QLabel(self)
        self.original_label.setAlignment(Qt.AlignCenter)
        self.left_layout.addWidget(self.original_label)

        self.select_button = QPushButton('选择图片', self)
        self.select_button.clicked.connect(self.open_image)
        self.left_layout.addWidget(self.select_button)

        self.main_layout.addLayout(self.left_layout)

        # 右侧布局：用于显示裁剪后的图像
        self.right_layout = QVBoxLayout()
        self.cropped_label = QLabel(self)
        self.cropped_label.setAlignment(Qt.AlignCenter)
        self.right_layout.addWidget(self.cropped_label)
        self.crop_button = QPushButton('裁剪', self)
        self.crop_button.clicked.connect(self.crop_image)
        self.right_layout.addWidget(self.crop_button)
        self.main_layout.addLayout(self.right_layout)
        self.setLayout(self.main_layout)

        # 初始化变量
        self.image_path = None
        self.image = None
        self.crop_rect = QRect()  # 裁剪矩形区域
        self.start_pos = QPoint()  # 开始位置
        self.end_pos = QPoint()  # 结束位置
        self.start_flag = False

    def open_image(self):
        min_size = min(self.cropped_label.size().height(), self.cropped_label.size().width())
        self.cropped_label.resize(min_size, min_size)

        """ 打开图片文件 """
        file_dialog = QFileDialog()
        self.image_path, _ = file_dialog.getOpenFileName(None, "选择图片", "", "Images (*.png *.xpm *.jpg)")
        if self.image_path:
            self.image = QImage(self.image_path)
            if self.image.isNull():
                QMessageBox.critical(self, "错误", f"无法加载图像: {self.image_path}")
                return

            self.update_original_image()

    def update_original_image(self):
        """ 更新左侧显示的原始图像 """
        pixmap = QPixmap.fromImage(self.image)
        print(pixmap.size())
        self.original_label.setPixmap(
            pixmap.scaled(self.original_label.size(), Qt.KeepAspectRatio, Qt.FastTransformation))

    def crop_image(self):
        """ 裁剪图像 """
        if not self.image or self.crop_rect.isEmpty():
            return

        cropped_image = self.image.copy(self.crop_rect)
        cropped_pixmap = QPixmap.fromImage(cropped_image)
        max_width, max_height = 16, 16  # 设定最大宽度和高度
        print(cropped_pixmap.size())

        cropped_pixmap = cropped_pixmap.scaled(max_width, max_height,
                                         aspectRatioMode=Qt.IgnoreAspectRatio,
                                         transformMode=Qt.FastTransformation)
        print(cropped_pixmap.size())
        print(self.cropped_label.size())
        self.cropped_label.setPixmap(
            cropped_pixmap.scaled(self.cropped_label.size(), Qt.KeepAspectRatio, Qt.FastTransformation))


    def mousePressEvent(self, event):
        """ 记录开始位置 """
        if event.button() == Qt.LeftButton and self.image and self.original_label.geometry().contains(event.pos()):
            self.start_pos = self.original_label.mapFromParent(event.pos())
            print(self.start_pos)
            # self.crop_rect.setTopLeft(self.original_label.mapTo(self.original_label, self.start_pos))
            self.crop_rect.setTopLeft(self.start_pos)

            self.crop_rect.setSize(QSize(0, 0))  # 初始大小为0
            self.start_flag = True
            print(self.original_label.pos())
    def mouseMoveEvent(self, event):
        """ 实时更新结束位置 """
        if self.image and self.start_flag:
            self.end_pos = self.original_label.mapFromParent(event.pos())
            # self.crop_rect.setBottomRight(self.original_label.mapTo(self.original_label, self.end_pos))
            self.crop_rect.setBottomRight(self.end_pos)
            self.update_original_image_with_crop_area()

    def mouseReleaseEvent(self, event):
        """ 确认裁剪区域 """
        if event.button() == Qt.LeftButton and self.start_flag:
            self.start_flag = False
            self.crop_rect.normalized()  # 确保坐标正确
            self.update_original_image_with_crop_area()

    def paintEvent(self, event):
        """
        绘制裁剪区域
        """
        if not self.image or self.crop_rect.isEmpty():
            return
        painter = QPainter(self.original_label.pixmap())
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(Qt.red, 2)
        painter.setPen(pen)
        # painter.drawRect(self.crop_rect)
        painter.end()

        self.original_label.update()

    def update_original_image_with_crop_area(self):
        """
        在原始图像上绘制裁剪区域
        """
        if not self.image:
            return

        original_pixmap = QPixmap.fromImage(self.image)
        painter = QPainter(original_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(Qt.red, 2)
        painter.setPen(pen)
        painter.drawRect(self.crop_rect)
        painter.end()

        self.original_label.setPixmap(
            original_pixmap.scaled(self.original_label.size(), Qt.KeepAspectRatio, Qt.FastTransformation))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageCropper()
    window.show()
    sys.exit(app.exec_())