import os

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow

from documentationWindow.documWnd import DocumentationUI
from finishWindow.finishGraphic import GraphicsDraw
from mainWindow.mainUI import MainUI
from processWindow.waitProcessUI import ProcessingWindow
from settingWindow.settingUI import SettingsUI
from prepareProcessWindow.showImageWnd import ShowImageWindow


class AppHandler(QMainWindow):

    def __init__(self):
        if not os.path.exists("./settings.json"):
            SettingsUI.create_settings_file()
        super().__init__()
        self.show_main_window()
        self.resize(600, 400)
        self.setWindowIcon(QIcon('icon.ico'))

    def show_main_window(self):
        new_widget = MainUI()
        new_widget.go_to_download_menu_sgnl.connect(self.show_download_menu)
        new_widget.go_to_documentation_sgnl.connect(
            self.show_documentation_wnd)
        new_widget.go_to_settings_sgnl.connect(self.show_settings_window)
        self.setWindowTitle("Главное меню")
        self.setCentralWidget(new_widget)

    def show_documentation_wnd(self):
        new_widget = DocumentationUI()
        new_widget.come_back_main_menu.connect(self.show_main_window)
        self.setWindowTitle("Документация")
        self.setCentralWidget(new_widget)

    def show_settings_window(self):
        new_widget = SettingsUI()
        new_widget.come_back_to_main_menu.connect(self.show_main_window)
        self.setWindowTitle("Настройки")
        self.setCentralWidget(new_widget)

    def show_download_menu(self, file_path="Файл не выбран", *args):
        new_widget = ShowImageWindow(file_path, *args)
        new_widget.get_new_image_sgnl.connect(self.show_download_menu)
        new_widget.go_to_processing_sgnl.connect(self.show_processing_window)
        new_widget.come_back_main_menu_sgnl.connect(self.show_main_window)
        self.setWindowTitle("Загрузочное меню")
        self.setCentralWidget(new_widget)

    def show_processing_window(self, file_path, *args):
        new_widget = ProcessingWindow(file_path, *args)
        new_widget.result_ready_sgnl.connect(self.show_finish_graphics)
        new_widget.go_to_download_menu_sgnl.connect(self.show_download_menu)
        self.setWindowTitle("Обработка изображения")
        self.setCentralWidget(new_widget)

    def show_finish_graphics(self, *args):
        new_widget = GraphicsDraw(*args)
        new_widget.come_back_to_download_menu_sgnl.connect(
            self.show_download_menu)
        self.setWindowTitle("График")
        self.setCentralWidget(new_widget)
