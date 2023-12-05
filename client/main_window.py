from PySide6 import QtCore
from PySide6.QtWidgets import QCheckBox, QDoubleSpinBox, QLabel, QLayout, QPushButton, QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QSpinBox, QComboBox, QDial
import requests

typeWidget = {
        int : QSpinBox,
        str : QLineEdit,
        list : QComboBox,
        float : QDoubleSpinBox,
        bool : QCheckBox,
}

class WidgetNames:
    age = "Возраст"
    gender = "Пол"
    ap_hi = "Верхнее давление"
    ap_lo = "Нижнее давление"
    cholesterol = "Уровень холестерин"
    gluc = "Уровень глюкозы"
    alcohol = "Употребляет алкоголь"
    smoke = "Курит"
    active = "Ведет активный образ жизни"
    bmi = "BMI"


class InputWidget(QWidget):
    class Row(QWidget):
        def __init__(self, widgets):
            super().__init__()
            self.hbox = QHBoxLayout()
            for widget in widgets:
                hbox = QHBoxLayout()
                hbox.addWidget(QLabel(widget[0]), 1)
                hbox.addWidget(widget[1], 3)
                self.hbox.addLayout(hbox)
            self.setLayout(self.hbox)

    def __init__(self, widgets):
        super().__init__()
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(QLabel("Введите данные пациента"))
        for i in range(0, 10, 3):
            self.vbox.addWidget(self.Row(widgets[i:i+3]))
        self.setLayout(self.vbox)


class WidgetKeeper:
    def __init__(self, widgets):
        self._widgets = []
        for widget in widgets:
            self._widgets.append((widget[0], typeWidget[widget[1]]()))

    def get_widgets(self):
        return self._widgets 


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout()
        self.setWindowTitle("dpppppp")
        self.vbox = QVBoxLayout()

        self.vbox.addWidget(QLabel("aboba"), 1) # header
        self.hbox = QHBoxLayout()
        
        widgets = [
                (WidgetNames.age, int),
                (WidgetNames.gender, bool),
                (WidgetNames.ap_hi, int),
                (WidgetNames.ap_lo, int),
                (WidgetNames.cholesterol, list),
                (WidgetNames.gluc, list),
                (WidgetNames.alcohol, bool),
                (WidgetNames.smoke, bool),
                (WidgetNames.active, bool),
                (WidgetNames.bmi, float),
        ]
        self.widget_keeper = WidgetKeeper(widgets)
        input_widget = InputWidget(self.widget_keeper.get_widgets())
        self.hbox.addWidget(input_widget)
        send_button = QPushButton("Send")
        send_button.clicked.connect(self.send)
        self.hbox.addWidget(send_button)
        self.vbox.addLayout(self.hbox, 3)
        
        self.main_layout.addLayout(self.vbox)

        self.setLayout(self.main_layout)

    def fetch_data(self):
        res = dict()
        for el in self.widget_keeper.get_widgets():
            res[el[0]] = el[1].text
        return res

    @QtCore.Slot()
    def send(self):
        r = requests.post("127.0.0.1:6969", json=self.fetch_data())
        print(r, r.json)

