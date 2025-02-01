import csv
import json
import numpy as np
import pandas as pd
import pyqtgraph as pg

from PyQt5.QtCore import Qt, QLocale, pyqtSignal
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QFileDialog, QHBoxLayout, QLabel

from finishWindow.finishUI import FinishImageWindow


class GraphicsDraw(QWidget):

    come_back_to_download_menu_sgnl = pyqtSignal()

    def __init__(self, file_path, info_drops):
        super().__init__()
        self.window_image = FinishImageWindow(file_path, info_drops)
        self.file_path = file_path
        self.info_drops = info_drops
        self.init_graph()
        self.prepare_data()

        self.setup_ui()
        self.setup_signals()

    def prepare_data(self):
        # get range from settings
        with open("./settings.json") as file:
            data = json.load(file)
            self.range = data.get("range", 0.2)

        self.diametrs = self.get_diameters(self.info_drops)
        counts, ranges = self.redo_range(
            self.diametrs, self.range)
        self.draw_graph(counts, ranges)

    def setup_vr_layout(self):
        self.vr_layout = QVBoxLayout()
        self.vr_layout.setContentsMargins(0, 0, 0, 0)
        self.vr_layout.setSpacing(0)
        self.vr_layout = QVBoxLayout()
        self.vr_layout.addLayout(self.hz_layout)
        self.vr_layout.addWidget(self.graphWidget)
        self.vr_layout.addLayout(self.layout_field_range)
        self.setLayout(self.vr_layout)

    def setup_up_hz_layout(self):
        self.hz_layout = QHBoxLayout()
        self.hz_layout.setContentsMargins(0, 0, 0, 0)
        self.hz_layout.setSpacing(4)

        self.hz_layout.addWidget(self.count_drops)
        self.hz_layout.addWidget(self.show_image_btn)
        self.hz_layout.addWidget(self.saving_btn)
        self.hz_layout.addWidget(self.come_back_to_download_menu_btn)

    def setup_field_layout(self):
        self.layout_field_range = QHBoxLayout()
        self.layout_field_range.addWidget(self.label_imgsz)
        self.layout_field_range.addWidget(self.line_edit)
        self.layout_field_range.addWidget(self.redraw_graphic_btn)
        self.layout_field_range.setAlignment(
            self.line_edit, Qt.AlignmentFlag.AlignLeft)

    def setup_ui(self):
        locale = QLocale(QLocale.Language.English,
                         QLocale.Country.UnitedStates)
        QLocale.setDefault(locale)

        self.count_drops = QLabel(self)
        self.count_drops.setText(f"Количество капель: {self.info_drops[0]}")

        self.show_image_btn = QPushButton("Посмотреть график")
        self.show_image_btn.setFixedSize(250, 30)

        self.saving_btn = QPushButton("Сохранить результаты")
        self.saving_btn.setFixedSize(250, 30)

        self.come_back_to_download_menu_btn = QPushButton(
            "Назад в меню загрузки")
        self.come_back_to_download_menu_btn.setFixedSize(250, 30)

        self.label_imgsz = QLabel(self)
        self.label_imgsz.setText("Шаг величины диаметра")
        self.label_imgsz.setMaximumWidth(200)
        self.line_edit = QLineEdit(self)
        self.line_edit.setText(str(self.range))
        self.older_line_edit = float(self.line_edit.text())
        self.line_edit.setMaximumWidth(150)
        validator = QDoubleValidator(0.0, 4000.0, 2, self)
        self.line_edit.setValidator(validator)

        self.redraw_graphic_btn = QPushButton("Перерисовать график")

        self.setup_field_layout()
        self.setup_up_hz_layout()
        self.setup_vr_layout()

    def setup_signals(self):
        self.show_image_btn.clicked.connect(self.toggle_window)
        self.saving_btn.clicked.connect(self.save_file)
        self.come_back_to_download_menu_btn.clicked.connect(
            self.come_back_to_download_menu_sgnl)
        self.redraw_graphic_btn.clicked.connect(self.redraw_graph)

    def redraw_graph(self):
        if float(self.line_edit.text()) != self.older_line_edit:
            counts, ranges = self.redo_range(
                self.diametrs, float(self.line_edit.text()))
            self.draw_graph(counts, ranges)
            self.older_line_edit = float(self.line_edit.text())

    def init_graph(self):
        self.graphWidget = pg.PlotWidget()
        self.legend = pg.LegendItem(offset=(-10, 50), labelTextSize='10pt', labelTextColor='w', pen=pg.mkPen(
            {'color': "white", 'width': 2}))
        self.legend.setParentItem(self.graphWidget.getPlotItem())

        item_y = pg.PlotDataItem(pen=None)
        item_x = pg.PlotDataItem(pen=None)

        self.legend.addItem(item_y, "По оси Y: Количество капель")
        self.legend.addItem(
            item_x, "По оси X: Промежуток значений диаметров капель (микроны)")

        self.graphWidget.setTitle(
            "Гистограмма распределения диаметров капель", size="15pt", color='w'
        )

        self.axis = VerticalAxisItem('bottom')

    def draw_graph(self, counts, ranges):
        x = np.arange(len(counts))

        bar_item = pg.BarGraphItem(
            x=x, height=counts, width=0.4, brush='r')

        self.graphWidget.clear()
        self.graphWidget.addItem(bar_item)

        for i in range(len(counts)):
            text = pg.TextItem(
                text=str(counts[i]), anchor=(0.5, 0.9))
            text.setPos(x[i], counts[i])
            self.graphWidget.addItem(text)

        ticks = [(i, f'{ranges[i]:.1f}-{ranges[i+1]:.1f}')
                 for i in range(len(ranges) - 1)]
        self.axis.setTicks([ticks])
        self.axis.setStyle(tickTextOffset=40)
        self.graphWidget.setAxisItems({'bottom': self.axis})

        self.graphWidget.setLabel(
            'bottom', "label", **{'color': 'rgba(255, 255, 255, 0%)', 'font-size': '20pt'})

    def get_diameters(self, info_drops):
        diametrs = [row[1] for row in info_drops[1]]
        diametrs.sort()
        return diametrs

    def redo_range(self, diametrs, range):
        ranges = np.arange(
            diametrs[0], diametrs[-1] + float(range), float(range))
        binned = pd.cut(diametrs, bins=ranges, right=False)
        counts = pd.Series(binned).value_counts().sort_index().tolist()
        return counts, ranges

    def save_file(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить CSV файл",
            "",
            "CSV файлы (*.csv);;Все файлы (*)"
        )
        if file_path:
            if not file_path.endswith(".csv"):
                file_path += ".csv"
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(
                    ["diametr (micrometer)", "coordinate center x", "coordinate center y"])
                for row in self.info_drops[1]:
                    writer.writerow([row[1]] + [row[2][0], row[2][1]])

    def toggle_window(self):
        if self.window_image.isVisible():
            self.window_image.hide()
        else:
            self.window_image.show()


class VerticalAxisItem(pg.AxisItem):
    def __init__(self, orientation, **kwargs):
        super().__init__(orientation, **kwargs)

    def drawPicture(self, p, axisSpec, tickSpecs, textSpecs):

        p.setRenderHint(p.RenderHint.Antialiasing, False)
        p.setRenderHint(p.RenderHint.TextAntialiasing, True)

        pen, p1, p2 = axisSpec
        p.setPen(pen)
        p.drawLine(p1, p2)

        for pen, p1, p2 in tickSpecs:
            p.setPen(pen)
            p.drawLine(p1, p2)

        if self.style['tickFont'] is not None:
            p.setFont(self.style['tickFont'])
        p.setPen(self.textPen())
        bounding = self.boundingRect().toAlignedRect()
        p.setClipRect(bounding)
        for rect, flags, text in textSpecs:
            p.save()  # save the painter state
            # move coordinate system to center of text rect
            p.translate(rect.center())
            p.rotate(-90)  # rotate text
            p.translate(-rect.center())  # revert coordinate system
            p.drawText(rect, int(flags), text)
            p.restore()
