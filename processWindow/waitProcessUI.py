import os
import uuid

from PyQt5.QtCore import Qt, pyqtSignal, QThread, QObject, pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QMessageBox
from PIL import Image

from scripts_yolo.model_method import processing_image


class ProcessingWindow(QWidget):

    result_ready_sgnl = pyqtSignal(str, tuple)
    go_to_download_menu_sgnl = pyqtSignal(str, float, float, bool, int, float)

    def __init__(self, file_path, *args):
        super().__init__()
        self.file_path = file_path
        self.args = args
        self.setup_ui()

        self.thread_procces = None
        self.worker_procces = None

    def setup_main_layout(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.advise_one_label)
        self.main_layout.addWidget(self.advise_two_label)

    def setup_ui(self):
        self.title_label = QLabel(
            "Идёт обработка изображения, пожалуйста, подождите..."
        )
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setWordWrap(True)
        self.title_label.setFixedHeight(50)

        self.advise_one_label = QLabel(
            "В случае долгой обработки или зависания программы закройте приложение и повторите обработку, поменяв параметры."
        )
        self.advise_one_label.setStyleSheet(
            "font-size: 16px; font-weight: 400;")
        self.advise_one_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setMinimumSize(300, 50)
        self.advise_one_label.setWordWrap(True)

        self.advise_two_label = QLabel(
            "Скорость обработки напрямую зависит от вычислительных характеристик вашего ПК."
        )
        self.advise_two_label.setStyleSheet(
            "font-size: 16px; font-weight: 400;")
        self.advise_two_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setFixedHeight(50)
        self.advise_two_label.setWordWrap(True)

        self.setup_main_layout()

        self.setLayout(self.main_layout)

    def showEvent(self, event):
        super().showEvent(event)
        self.setup_thread()

    def setup_thread(self):
        self.thread_procces = QThread()
        self.worker_procces = WorkerProcces(self.file_path, self.args)
        self.worker_procces.moveToThread(self.thread_procces)
        self.worker_procces.error_call.connect(self.show_mistake)
        self.thread_procces.started.connect(self.worker_procces.run)
        self.worker_procces.result_ready.connect(self.result_ready_sgnl)
        self.worker_procces.finished.connect(self.thread_procces.quit)
        self.worker_procces.finished.connect(self.worker_procces.deleteLater)
        self.thread_procces.finished.connect(self.thread_procces.deleteLater)
        self.thread_procces.start()

    def show_mistake(self, info_error):
        self.go_to_download_menu_sgnl.emit(self.file_path, *self.args)
        QMessageBox.information(self, "Erorr", f"{info_error}")


# Class for manage thread
class WorkerProcces(QObject):

    result_ready = pyqtSignal(str, tuple)
    finished = pyqtSignal()
    error_call = pyqtSignal(str)

    def __init__(self, file_path, args):
        super().__init__()
        self.file_path = file_path
        self.args = args

    # start processing model
    def run(self):
        try:
            path_formate_image = self.find_filled_areas(self.file_path)
            result = processing_image(path_formate_image, *self.args)
            if result[0] == 0:
                raise Exception("Модель не нашла ни одного объекта")
            self.result_ready.emit(path_formate_image, result)
        except Exception as e:
            self.error_call.emit(f"{e}")
        finally:
            self.finished.emit()

    #  delete black area on image and save image in ./tmp
    def find_filled_areas(self, file_path):
        with Image.open(file_path) as img:
            gray_image = img.convert("L")
            threshold = 30
            bw_image = gray_image.point(lambda p: p > threshold and 255)
            bbox = bw_image.getbbox()

            if bbox:
                gray_image = img.crop(bbox)

            if not os.path.exists("./tmp"):
                os.makedirs("./tmp")

            filename = f"{uuid.uuid4()}.jpg"
            temp_file_path = f"./tmp/{filename}"
            gray_image.save(temp_file_path)
            return temp_file_path
