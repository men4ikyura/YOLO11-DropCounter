from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget, QLabel, QFileDialog, QSpacerItem, QSizePolicy


class MainUI(QWidget):

    go_to_download_menu_sgnl = pyqtSignal(str)
    go_to_documentation_sgnl = pyqtSignal()
    go_to_settings_sgnl = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_signals()

    def setup_main_layout(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(
            self.download_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(
            self.documentation_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(
            self.setting_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addItem(QSpacerItem(
            10, 30, QSizePolicy.Minimum, QSizePolicy.Fixed))
        self.main_layout.addWidget(
            self.title, alignment=Qt.AlignmentFlag.AlignCenter)

    def setup_ui(self):
        self.download_btn = QPushButton("Загрузить изображение")
        self.download_btn.setFixedSize(300, 30)

        self.documentation_btn = QPushButton("Документация")
        self.documentation_btn.setFixedSize(300, 30)

        self.setting_btn = QPushButton("Настройки приложения")
        self.setting_btn.setFixedSize(300, 30)

        self.title = QLabel(
            "    Приложение \"Voshod\" для подсчета капель на изображении с помощью технологии YOLOv11.\n"
            "    Загрузите изображение и начните обработку.\n"
            "    Далее, после обработки вам будет доступна такая информация как: количество капель, "
            "график распределения диаметров капель.\n"
            "    Также будет возможность сохранить результаты в csv файл."
        )
        self.title.setWordWrap(True)
        self.title.setMinimumSize(400, 150)

        self.setup_main_layout()

        self.setLayout(self.main_layout)

    def setup_signals(self):
        self.setting_btn.clicked.connect(self.go_to_settings_sgnl)
        self.download_btn.clicked.connect(self.open_file)
        self.documentation_btn.clicked.connect(
            self.go_to_documentation_sgnl)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите файл", "", "Images (*.png *.jpg)")
        if file_path:
            self.go_to_download_menu_sgnl.emit(file_path)
