from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap, QPainter, QPolygon, QPen, QColor, QGuiApplication
from PyQt5.QtCore import Qt, QPoint, QSize
from PIL import Image


class FinishImageWindow(QWidget):

    def __init__(self, file_path, info_drops):
        super().__init__()
        self.file_path = file_path
        self.info_drops = info_drops
        self.setup_ui()

    def setup_main_vr_layout(self):
        self.vr_layout = QVBoxLayout()
        self.vr_layout.setContentsMargins(0, 0, 0, 0)
        self.vr_layout.setSpacing(0)
        self.vr_layout.addWidget(self.count_drops)
        width_file, height_file, koef = self.count_sizes(self.file_path)
        self.width_window, self.height_window = width_file, height_file + 50
        custom_widget = CustomPaintWidget(
            self.file_path, self.info_drops, koef, width_file, height_file)
        self.vr_layout.addWidget(custom_widget)
        self.setLayout(self.vr_layout)

    def setup_ui(self):
        self.count_drops = QLabel(self)
        self.count_drops.setText(f"Количество капель: {self.info_drops[0]}")
        self.count_drops.setFixedHeight(30)

        self.setup_main_vr_layout()

    def sizeHint(self):
        return QSize(self.width_window, self.height_window)

    def count_sizes(self, file_path):
        screen = QGuiApplication.primaryScreen()

        screen_size = screen.geometry()
        width_screen = screen_size.width() - 500
        height_screen = screen_size.height() - 300

        with Image.open(file_path) as img:
            width_file, height_file = img.size

        less_width = width_file <= width_screen
        less_height = height_file <= height_screen

        if less_width and less_height:
            koef = 1
        else:
            koef_width = width_screen / width_file
            koef_height = height_screen / height_file
            koef = min(koef_width, koef_height)

        new_width_file = int(width_file * koef)
        new_height_file = int(height_file * koef)

        return new_width_file, new_height_file, koef


class CustomPaintWidget(QWidget):
    def __init__(self, file_path, info_drops, koef, width_file, height_file):
        super().__init__()
        self.file_path = file_path
        self.info_drops = info_drops
        self.koef = koef
        self.width_file = width_file
        self.height_file = height_file

    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap(self.file_path)
        scaled_pixmap = pixmap.scaled(
            self.width_file,
            self.height_file,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        painter.drawPixmap(0, 0, scaled_pixmap)

        pen_line = QPen()
        pen_line.setWidth(3)
        pen_line.setColor(QColor(0, 128, 255))
        painter.setPen(pen_line)

        for info in self.info_drops[1]:
            masks = []
            for coordinate in info[0]:
                masks.append(
                    QPoint(int(coordinate[0] * self.koef), int(coordinate[1] * self.koef)))
            masks.append(
                QPoint(int(info[0][0][0] * self.koef), int(info[0][0][1] * self.koef)))
            center = QPoint(int(info[2][0] * self.koef),
                            int(info[2][1] * self.koef))
            painter.drawEllipse(center, 2, 2)
            polygon = QPolygon(masks)
            painter.drawPolyline(polygon)

        painter.end()
