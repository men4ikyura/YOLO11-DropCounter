from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QScrollArea


class DocumentationUI(QWidget):

    come_back_main_menu = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_signals()

    def setup_main_layout(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.area)
        self.main_layout.addWidget(self.come_back_main_menu_btn)
        self.setLayout(self.main_layout)

    def setup_ui(self):
        self.come_back_main_menu_btn = QPushButton("Назад")
        self.come_back_main_menu_btn.setFixedWidth(200)

        self.text = """
        <h2>Параметры для настройки модели обнаружения объектов</h2>
        <h3>1. <b>conf</b> — Порог уверенности обнаружения объекта</h3>
        <p><b>Описание:</b> Указывает минимальный уровень уверенности модели для обнаружения объекта. Если уверенность ниже этого значения, объект будет проигнорирован.</p>
        <p><b>Тип значения:</b> Дробное число от 0 до 1.</p>
        <p><b>Рекомендации:</b></p>
        <ul>
            <li><b>Не рекомендуется</b> устанавливать значение:
                <ul>
                    <li><b>Меньше 0.1</b> — может значительно снизить скорость обработки из-за ложных срабатываний.</li>
                    <li><b>Больше 0.9</b> — может привести к пропуску значительной части объектов и снижению точности.</li>
                </ul>
            </li>
        </ul>

        <h3>2. <b>iou</b> — Порог пересечения объектов</h3>
        <p><b>Описание:</b> Определяет, как модель обрабатывает пересекающиеся объекты.</p>
        <ul>
            <li>При <b>низких значениях</b> из двух пересекающихся объектов будет выделен только один.</li>
            <li>При <b>высоких значениях</b> будут выделены оба объекта.</li>
        </ul>
        <p><b>Тип значения:</b> Дробное число от 0 до 1.</p>

        <h3>3. <b>imgsz</b> — Размер входного изображения</h3>
        <p><b>Описание:</b> Определяет размер изображения, которое подается на вход модели. Изображение будет сжато до размеров <b>imgsz × imgsz</b> пикселей.</p>
        <p><b>Тип значения:</b> Целое число больше нуля.</p>
        <p><b>Значение по умолчанию:</b> 640.</p>
        <p><b>Рекомендации:</b></p>
        <ul>
            <li>Устанавливать значение, которое делится на 32.</li>
            <li>Если нужно повысить точность обработка изображения, увеличьте значение до <b>1280</b>.</li>
        </ul>

        <h3>4. <b>retina_masks</b> — Точность контуров объекта</h3>
        <p><b>Описание:</b> Определяет уровень детализации контуров объекта.</p>
        <ul>
            <li>При значении <b>True</b> контуры капель будут более точными, что улучшит вычисление их размеров.</li>
            <li>При значении <b>False</b> контуры будут менее детализированными, но скорость обработки увеличится.</li>
        </ul>
        <p><b>Тип значения:</b> Логическое (<b>True</b> или <b>False</b>).</p>
        <p><b>Рекомендации:</b> Если обработка происходит медленно или возникают ошибки, отключите параметр (<b>False</b>), чтобы повысить скорость работы модели.</p>
        """

        self.scrollAreaWidgetContents = QLabel(self.text, self)
        self.scrollAreaWidgetContents.setWordWrap(True)
        self.scrollAreaWidgetContents.setAlignment(
            Qt.AlignCenter)
        self.scrollAreaWidgetContents.adjustSize()

        self.area = QScrollArea(self)
        self.area.setWidgetResizable(True)
        self.area.setWidget(self.scrollAreaWidgetContents)

        self.setup_main_layout()

    def setup_signals(self):
        self.come_back_main_menu_btn.clicked.connect(
            self.come_back_main_menu)
