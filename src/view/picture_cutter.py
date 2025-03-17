from PyQt5 import uic
from PyQt5.QtCore import QRect, QPoint, Qt, QSize
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox, QWidget, QPushButton, QLabel, QMainWindow, \
    QCheckBox, QLineEdit

from file import load_texture_from_file
from tools.label_tool import getPixmapPoint, adjust_position, rect_overflow_clear
from tools.load import get_ui_path, get_img_by_name, get_img_path


class PictureCutter(QWidget):
    input_img_label: QLabel
    input_img_button: QPushButton
    output_img_label: QLabel
    output_img_button: QPushButton
    pixmap: QPixmap
    image_path: any = None
    image: QImage
    original_crop_rect: QRect = QRect()
    target_crop_rect: QRect = QRect()
    default_output_img_size:QSize() = QSize(16, 16)
    check_pix_fixed: QCheckBox
    check_use_linear: QCheckBox
    x_edit: QLineEdit
    y_edit: QLineEdit

    def __init__(self):
        super().__init__()
        uic.loadUi(get_ui_path('picture_cutter.ui'), self)
        self.setMouseTracking(True)
        self.start_flag = False
        self.input_img_button.clicked.connect(self.open_image)
        self.output_img_button.clicked.connect(self.crop_image)
        self.image = get_img_by_name('img.png')
        self.check_pix_fixed.setChecked(True)
        self.x_edit.setText(self.default_output_img_size.width().__str__())
        self.y_edit.setText(self.default_output_img_size.height().__str__())

    def showEvent(self, event):
        # 在这里执行需要根据实际尺寸调整的操作
        self.resizeEvent(None)

    def resizeEvent(self, event):

        self.update_image_show()
        return

    def open_image(self):
        """ 打开图片文件 """
        file_dialog = QFileDialog()
        self.image_path, _ = file_dialog.getOpenFileName(None, "选择图片", "", "Images (*.png *.xpm *.jpg)")
        if self.image_path:
            self.image = QImage(self.image_path)
            if self.image.isNull():
                QMessageBox.critical(self, "错误", f"无法加载图像: {self.image_path}")
                return
            self.update_image_show()

    def update_image_show(self):
        """ 更新左侧显示的原始图像 """
        self.pixmap = QPixmap.fromImage(self.image)
        self.pixmap = self.pixmap.scaled(self.input_img_label.size(), Qt.KeepAspectRatio, Qt.FastTransformation)
        if self.original_crop_rect:
            self.target_crop_rect.setTopLeft(adjust_position(self.image, self.pixmap, self.original_crop_rect.topLeft()))
            self.target_crop_rect.setBottomRight(adjust_position(self.image, self.pixmap, self.original_crop_rect.bottomRight()))
            self.crop_image()
        self.input_img_label.setPixmap(self.pixmap)

    def crop_image(self):
        """ 裁剪图像 """
        if not self.image or self.original_crop_rect.isEmpty():
            return

        cropped_image = self.image.copy(self.original_crop_rect)
        cropped_pixmap = QPixmap.fromImage(cropped_image)
        max_width, max_height = 16, 16  # 设定最大宽度和高度
        crop_size = cropped_pixmap.size()
        if self.check_pix_fixed.isChecked():
            try:
                crop_size = QSize(int(self.x_edit.text()), int(self.y_edit.text()))
            except ValueError:
                crop_size = self.default_output_img_size
                self.x_edit.setText(self.default_output_img_size.width().__str__())
                self.y_edit.setText(self.default_output_img_size.height().__str__())
                pass
        transform_mode = Qt.FastTransformation
        if self.check_use_linear.isChecked():
            transform_mode = Qt.SmoothTransformation
        cropped_pixmap = cropped_pixmap.scaled(crop_size,
                                         aspectRatioMode=Qt.IgnoreAspectRatio,
                                         transformMode=transform_mode)

        self.output_img_label.setPixmap(
            cropped_pixmap.scaled(self.input_img_label.size(), Qt.KeepAspectRatio, Qt.FastTransformation))

    def mousePressEvent(self, event):
        """ 记录开始位置 """
        global_pos = event.globalPos()
        local_pos_input = self.input_img_label.mapFromGlobal(global_pos)
        if event.button() == Qt.LeftButton and self.input_img_label.rect().contains(local_pos_input):
            start_pos = getPixmapPoint(self.input_img_label, local_pos_input)
            self.target_crop_rect.setTopLeft(start_pos)
            self.target_crop_rect.setSize(QSize(0, 0))
            self.original_crop_rect.setTopLeft(adjust_position(self.pixmap, self.image, start_pos))
            self.start_flag = True

    def mouseMoveEvent(self, event):
        """ 实时更新结束位置 """
        if self.start_flag:
            global_pos = event.globalPos()
            local_pos_input = self.input_img_label.mapFromGlobal(global_pos)
            end_pos = getPixmapPoint(self.input_img_label, local_pos_input)
            self.target_crop_rect.setBottomRight(end_pos)
            self.original_crop_rect.setBottomRight(adjust_position(self.pixmap, self.image, end_pos))
            self.update_original_image_with_crop_area()

    def mouseReleaseEvent(self, event):
        """ 确认裁剪区域 """
        if event.button() == Qt.LeftButton and self.start_flag:
            self.start_flag = False
            self.target_crop_rect.normalized()  # 确保坐标正确
            self.update_original_image_with_crop_area()
            self.crop_image()

    def paintEvent(self, event):
        """
        绘制裁剪区域
        """
        if not self.image or self.target_crop_rect.isEmpty():
            return
        painter = QPainter(self.input_img_label.pixmap())
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(Qt.black, 2)
        if self.start_flag:
            pen = QPen(Qt.red, 2)
        painter.setPen(pen)
        rect_overflow_clear(self.target_crop_rect, self.pixmap)
        rect_overflow_clear(self.original_crop_rect, self.image)
        painter.drawRect(self.target_crop_rect)
        painter.end()

    def update_original_image_with_crop_area(self):
        """
        在原始图像上绘制裁剪区域
        """
        if not self.pixmap:
            return
        self.input_img_label.setPixmap(self.pixmap)

if __name__ == '__main__':
    app = QApplication([])
    ex = PictureCutter()
    ex.show()
    app.exec_()