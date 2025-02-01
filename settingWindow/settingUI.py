import json

from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtCore import Qt, QLocale, pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QSlider, QHBoxLayout, QLineEdit, QCheckBox, QFileDialog, QMessageBox


class SettingsUI(QWidget):

    come_back_to_main_menu = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.settings_params = self.load_settings()
        self.model_path = self.settings_params.get("model_path", None)
        self.setup_ui()
        self.setup_signals()

    def setup_iou(self):
        self.iou = self.settings_params.get("iou", 0.7)
        self.slider_iou = QSlider(Qt.Orientation.Horizontal, self)
        self.slider_iou.setMaximumWidth(150)
        self.slider_iou.setRange(0, 100)
        self.slider_iou.setValue(int(self.iou*100))
        self.slider_iou.valueChanged.connect(self.update_iou)
        self.result_label_iou = QLabel(f'iou: {self.iou}', self)
        self.result_label_iou.setFixedWidth(80)
        self.label_iou = QHBoxLayout()
        self.label_iou.addWidget(self.result_label_iou)
        self.label_iou.addWidget(self.slider_iou)
        self.label_iou.setAlignment(
            self.slider_iou, Qt.AlignmentFlag.AlignLeft)

    def setup_conf(self):
        self.conf = self.settings_params.get("conf", 0.25)
        self.slider_conf = QSlider(Qt.Orientation.Horizontal, self)
        self.slider_conf.setMaximumWidth(150)
        self.slider_conf.setRange(0, 100)
        self.slider_conf.setValue(int(self.conf*100))
        self.slider_conf.valueChanged.connect(self.update_conf)
        self.result_label_conf = QLabel(f'conf: {self.conf}', self)
        self.result_label_conf.setFixedWidth(80)
        self.label_conf = QHBoxLayout()
        self.label_conf.addWidget(self.result_label_conf)
        self.label_conf.addWidget(self.slider_conf)
        self.label_conf.setAlignment(
            self.slider_conf, Qt.AlignmentFlag.AlignLeft)

    def setup_imgsz(self):
        self.imgsz = self.settings_params.get("imgsz", 640)
        self.result_label_imgsz = QLabel(self)
        self.result_label_imgsz.setText("imgsz")
        self.result_label_imgsz.setMaximumWidth(50)
        self.line_edit_imgsz = QLineEdit()
        self.line_edit_imgsz.setText(str(self.imgsz))
        self.line_edit_imgsz.setMaximumWidth(150)
        validator = QIntValidator(0, 4000, self)
        self.line_edit_imgsz.setValidator(validator)
        self.label_imgsz = QHBoxLayout()
        self.label_imgsz.addWidget(self.result_label_imgsz)
        self.label_imgsz.addWidget(self.line_edit_imgsz)
        self.label_imgsz.setAlignment(
            self.line_edit_imgsz, Qt.AlignmentFlag.AlignLeft)

    def setup_pixels(self):
        self.pixels = self.settings_params.get("pixels", 7.5)
        self.result_label_pixels = QLabel(self)
        self.result_label_pixels.setText("Количесвто пикселей в микроне")
        self.result_label_pixels.setMaximumWidth(250)
        self.line_edit_pixels = QLineEdit(self)
        self.line_edit_pixels.setText(str(self.pixels))
        self.line_edit_pixels.setMaximumWidth(150)
        validator = QDoubleValidator(0.0, 50.0, 2, self)
        validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        validator.setRange(0.0, 50.0, 2)
        self.line_edit_pixels.setValidator(validator)
        self.label_pixels = QHBoxLayout()
        self.label_pixels.addWidget(self.result_label_pixels)
        self.label_pixels.addWidget(self.line_edit_pixels)
        self.label_pixels.setAlignment(
            self.line_edit_pixels, Qt.AlignmentFlag.AlignLeft)

    def setup_range(self):
        self.range = self.settings_params.get("range", 0.2)
        self.result_label_range = QLabel(self)
        self.result_label_range.setText("Шаг величины диаметра (микроны)")
        self.result_label_range.setMaximumWidth(300)
        self.line_edit_range = QLineEdit(self)
        self.line_edit_range.setText(str(self.range))
        self.line_edit_range.setMaximumWidth(150)
        validator = QDoubleValidator(0.0, 50.0, 2, self)
        validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        validator.setRange(0.0, 50.0, 2)
        self.line_edit_range.setValidator(validator)
        self.label_range = QHBoxLayout()
        self.label_range.addWidget(self.result_label_range)
        self.label_range.addWidget(self.line_edit_range)
        self.label_range.setAlignment(
            self.line_edit_range, Qt.AlignmentFlag.AlignLeft)

    def setup_retina_masks(self):
        self.retina_masks = self.settings_params.get("retina_masks", False)
        self.retina_masks_box = QCheckBox("retina_masks")
        self.retina_masks_box.setChecked(self.retina_masks)

    def setup_path_model_label(self):
        self.model_label = QLabel(self)
        self.model_label.setText(f"Путь до модели: {self.model_path}")
        self.model_label.setWordWrap(True)
        self.model_label.setMinimumHeight(100)
        self.model_label.adjustSize()
        self.get_path_to_model_btn = QPushButton("Выбрать модель")
        self.get_path_to_model_btn.setFixedSize(200, 30)
        self.model_layout = QHBoxLayout()
        self.model_layout.addWidget(self.model_label)
        self.model_layout.addWidget(
            self.get_path_to_model_btn)

    def setup_main_layout(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.setSpacing(20)
        self.main_layout.addWidget(
            self.title, alignment=Qt.AlignmentFlag.AlignCenter)

        self.main_layout.addLayout(
            self.label_conf)

        self.main_layout.addLayout(
            self.label_iou)

        self.main_layout.addWidget(
            self.retina_masks_box,  alignment=Qt.AlignmentFlag.AlignLeft)

        self.main_layout.addLayout(
            self.label_imgsz)

        self.main_layout.addLayout(
            self.label_pixels)

        self.main_layout.addLayout(
            self.label_range)

        self.main_layout.addLayout(
            self.model_layout)

        self.main_layout.addWidget(self.save_settings_button,
                                   alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.come_back_main_menu_btn,
                                   alignment=Qt.AlignmentFlag.AlignCenter)

    def setup_ui(self):
        locale = QLocale(QLocale.Language.English,
                         QLocale.Country.UnitedStates)
        QLocale.setDefault(locale)

        self.come_back_main_menu_btn = QPushButton("Назад")
        self.come_back_main_menu_btn.setFixedSize(300, 30)

        self.save_settings_button = QPushButton("Сохранить настройки")
        self.save_settings_button.setFixedSize(300, 30)

        self.setup_conf()
        self.setup_iou()
        self.setup_imgsz()
        self.setup_pixels()
        self.setup_retina_masks()
        self.setup_range()
        self.setup_path_model_label()

        self.title = QLabel("Установите параметры модели по умолчанию")
        self.title.setStyleSheet("font-size: 14px; font-weight: bold;")

        self.setup_main_layout()

        self.setLayout(self.main_layout)

    def update_conf(self, value):
        self.result_label_conf.setText(f'conf: {value / 100}')

    def update_iou(self, value):
        self.result_label_iou.setText(f'iou: {value / 100}')

    def load_settings(self):
        with open("./settings.json") as file:
            return json.load(file)

    def check_valid_param(self):
        return self.line_edit_imgsz.text() != '' and self.line_edit_pixels.text() != '' and self.line_edit_range.text() != ''

    def update_parametrs(self):
        if not self.check_valid_param():
            QMessageBox.information(
                self, "Предупреждение", "Заполните поля данными")
        else:
            with open("./settings.json", "w") as file:
                new_parametrs = {
                    "iou": self.slider_iou.value() / 100,
                    "conf": self.slider_conf.value() / 100,
                    "retina_masks": self.retina_masks_box.isChecked(),
                    "imgsz": self.line_edit_imgsz.text(),
                    "pixels": self.line_edit_pixels.text(),
                    "range": self.line_edit_range.text(),
                    "model_path": self.model_path
                }
                json.dump(new_parametrs, file, ensure_ascii=False,  indent=4)
                QMessageBox.information(self, "Успешно", "Настройки сохранены")

    def open_model(self):
        self.model_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите путь до модели", "", "Images (*)")
        if self.model_path:
            self.model_label.setText(f"Путь до модели: {self.model_path}")

    def setup_signals(self):
        self.get_path_to_model_btn.clicked.connect(self.open_model)
        self.come_back_main_menu_btn.clicked.connect(
            self.come_back_to_main_menu)
        self.save_settings_button.clicked.connect(self.update_parametrs)

    @staticmethod
    def create_settings_file():
        with open("./settings.json", "w") as file:
            default_parametrs = {
                "iou": 0.7,
                "conf": 0.25,
                "retina_masks": False,
                "imgsz": 640,
                "pixels": 7.5,
                "range": 0.2,
                "model_path": None
            }
            json.dump(default_parametrs, file, ensure_ascii=False,  indent=4)
