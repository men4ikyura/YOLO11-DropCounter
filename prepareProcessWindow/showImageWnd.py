import json

from PyQt5.QtGui import QPixmap, QIntValidator, QDoubleValidator
from PyQt5.QtCore import Qt, QLocale, pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QSlider, QCheckBox, QLineEdit, QHBoxLayout, QFileDialog, QMessageBox


class ShowImageWindow(QWidget):

    get_new_image_sgnl = pyqtSignal(str, float, float, bool, str, str)
    go_to_processing_sgnl = pyqtSignal(str, float, float, bool, int, float)
    come_back_main_menu_sgnl = pyqtSignal()

    def __init__(self,  file_path, *params):
        super().__init__()
        self.file_path = file_path
        self.params = self.load_processing_params() if not params else params
        self.setup_ui()
        self.setup_signals()

    def setup_before_process_image_ui(self):
        if self.file_path:
            pixmap = QPixmap(self.file_path)
            width, height = 300, 300
            scaled_pixmap = pixmap.scaled(
                width, height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            image_label = QLabel(self)
            image_label.setPixmap(scaled_pixmap)
            self.main_layout.addWidget(
                image_label, alignment=Qt.AlignmentFlag.AlignCenter)

    def update_iou(self, value):
        self.result_label_iou.setText(f'iou: {value / 100}')

    def update_conf(self, value):
        self.result_label_conf.setText(f'conf: {value / 100}')

    def setup_conf(self):
        self.slider_conf = QSlider(Qt.Orientation.Horizontal, self)
        self.slider_conf.setMaximumWidth(150)
        self.slider_conf.setRange(0, 100)
        self.slider_conf.setValue(int(self.params[0]*100))
        self.slider_conf.valueChanged.connect(self.update_conf)
        self.result_label_conf = QLabel(f'conf: {self.params[0]}', self)
        self.result_label_conf.setFixedWidth(80)
        self.label_conf = QHBoxLayout()
        self.label_conf.addWidget(self.result_label_conf)
        self.label_conf.addWidget(self.slider_conf)
        self.label_conf.setAlignment(
            self.slider_conf, Qt.AlignmentFlag.AlignLeft)

    def setup_iou(self):
        self.slider_iou = QSlider(Qt.Orientation.Horizontal, self)
        self.slider_iou.setMaximumWidth(150)
        self.slider_iou.setRange(0, 100)
        self.slider_iou.setValue(int(self.params[1]*100))
        self.slider_iou.valueChanged.connect(self.update_iou)
        self.result_label_iou = QLabel(f'iou: {self.params[1]}', self)
        self.result_label_iou.setFixedWidth(80)
        self.label_iou = QHBoxLayout()
        self.label_iou.addWidget(self.result_label_iou)
        self.label_iou.addWidget(self.slider_iou)
        self.label_iou.setAlignment(
            self.slider_iou, Qt.AlignmentFlag.AlignLeft)

    def setup_imgsz(self):
        self.label_imgsz = QLabel(self)
        self.label_imgsz.setText("imgsz")
        self.label_imgsz.setMaximumWidth(50)
        self.line_edit_imgsz = QLineEdit(self)
        self.line_edit_imgsz.setText(str(self.params[3]))
        self.line_edit_imgsz.setMaximumWidth(150)
        validator = QIntValidator(0, 4000, self)
        self.line_edit_imgsz.setValidator(validator)
        self.layout_imgsz = QHBoxLayout()
        self.layout_imgsz.addWidget(self.label_imgsz)
        self.layout_imgsz.addWidget(self.line_edit_imgsz)
        self.layout_imgsz.setAlignment(
            self.line_edit_imgsz, Qt.AlignmentFlag.AlignLeft)

    def setup_pixels(self):
        self.label_px = QLabel(self)
        self.label_px.setText("Количесвто пикселей в микроне")
        self.label_px.setMaximumWidth(250)
        self.line_edit_px = QLineEdit(self)
        self.line_edit_px.setText(str(self.params[4]))
        self.line_edit_px.setMaximumWidth(150)
        validator = QDoubleValidator(0.0, 50.0, 2, self)
        validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        validator.setRange(0.0, 50.0, 2)
        self.line_edit_px.setValidator(validator)
        self.layout_px = QHBoxLayout()
        self.layout_px.addWidget(self.label_px)
        self.layout_px.addWidget(self.line_edit_px)
        self.layout_px.setAlignment(
            self.line_edit_px, Qt.AlignmentFlag.AlignLeft)

    def setup_retina_masks(self):
        self.retina_masks_box = QCheckBox("retina_masks")
        self.retina_masks_box.setChecked(self.params[2])

    def setup_main_layout(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.setSpacing(20)

        self.main_layout.addWidget(
            self.file_label)
        self.main_layout.addWidget(
            self.text)

        self.main_layout.addLayout(
            self.label_conf)

        self.main_layout.addLayout(
            self.label_iou)

        self.main_layout.addWidget(
            self.retina_masks_box)

        self.main_layout.addLayout(
            self.layout_imgsz)

        self.main_layout.addLayout(
            self.layout_px)

        self.setup_before_process_image_ui()

        self.main_layout.addWidget(
            self.start_process_image_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(
            self.get_new_file_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(
            self.come_back_main_menu_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    def setup_ui(self):
        locale = QLocale(QLocale.Language.English,
                         QLocale.Country.UnitedStates)
        QLocale.setDefault(locale)

        self.file_label = QLabel(self)
        self.file_label.setText(f"Выбранный файл: {self.file_path}")
        self.file_label.setWordWrap(True)
        self.file_label.adjustSize()
        self.text = QLabel(self)
        self.text.setText("Выберите параметры обработки:")

        self.setup_conf()
        self.setup_iou()
        self.setup_imgsz()
        self.setup_pixels()
        self.setup_retina_masks()

        self.start_process_image_btn = QPushButton(
            "Начать обработку изображения")
        self.start_process_image_btn.setFixedSize(300, 30)

        self.get_new_file_btn = QPushButton("Выбрать другой файл")
        self.get_new_file_btn.setFixedSize(300, 30)

        self.come_back_main_menu_btn = QPushButton("Главное меню")
        self.come_back_main_menu_btn.setFixedSize(300, 30)

        self.setup_main_layout()

        self.setLayout(self.main_layout)

    def load_processing_params(self):
        with open("./settings.json") as file:
            data = json.load(file)
            return (data.get("conf", 0.25), data.get("iou", 0.7), data.get(
                "retina_masks", False), data.get("imgsz", 640), data.get("pixels", 7.5))

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите файл", "", "Images (*.png *.jpg *jpeg)")
        if file_path:
            self.get_new_image_sgnl.emit(file_path, self.slider_conf.value() / 100, self.slider_iou.value(
            ) / 100, self.retina_masks_box.isChecked(), self.line_edit_imgsz.text(), self.line_edit_px.text())

    def check_valid_param(self):
        return self.line_edit_imgsz.text() != '' and self.line_edit_px.text() != ''

    def go_to_processing(self):
        if not self.check_valid_param():
            QMessageBox.information(
                self, "Предупреждение", "Заполните поля данными")
        else:
            self.go_to_processing_sgnl.emit(self.file_path, self.slider_conf.value() / 100, self.slider_iou.value(
            ) / 100, self.retina_masks_box.isChecked(), int(self.line_edit_imgsz.text()), float(self.line_edit_px.text()))

    def setup_signals(self):
        if self.file_path != "Файл не выбран":
            self.start_process_image_btn.clicked.connect(
                self.go_to_processing)

        self.get_new_file_btn.clicked.connect(self.open_file)

        self.come_back_main_menu_btn.clicked.connect(
            self.come_back_main_menu_sgnl)
