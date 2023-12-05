from PySide6 import QtCore
from PySide6.QtWidgets import QCheckBox, QDoubleSpinBox, QLabel, QLayout, QPushButton, QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QSpinBox, QComboBox, QDial

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
        widget_keeper = WidgetKeeper(widgets)
        input_widget = InputWidget(widget_keeper.get_widgets())
        self.hbox.addWidget(input_widget)
        send_button = QPushButton("Send")
        send_button.clicked.connect(self.send)
        self.hbox.addWidget(send_button)
        self.vbox.addLayout(self.hbox, 3)
        
        # self.left_vbox = QVBoxLayout()
        # self.right_vbox = QVBoxLayout()
        #
        # self.tables_list = TablesList()
        # self.entries_table = EntriesTable()
        # self.entry_manager: EntryManager | None = None
        #
        # update_tables_button = QPushButton("update")
        # update_tables_button.clicked.connect(self.update_tables_list)
        #
        # self.create_entry_button = QPushButton("create")
        # self.create_entry_button.clicked.connect(self.create_entry_manager_for_create)
        # self.create_entry_button.hide()
        #
        # self.left_vbox.addWidget(update_tables_button)
        # self.left_vbox.addWidget(self.tables_list)
        # self.right_vbox.addWidget(self.entries_table)
        # self.right_vbox.addWidget(self.create_entry_button)
        # self.hbox.addLayout(self.left_vbox, 1)
        # self.hbox.addLayout(self.right_vbox, 3)
        self.main_layout.addLayout(self.vbox)

        self.setLayout(self.main_layout)

        # self.tables_list.doubleClicked.connect(self.update_entries_table)
        # self.entries_table.select_data_signal.connect(self.create_entry_manager_for_update)

        # self.database = database.Database() 

    @QtCore.Slot()
    def send(self):
        self.clear_layout(self.main_layout)
        print("hello")

    def clear_layout(self, layout):
        for x in reversed(range(layout.count())):
            widget = layout.takeAt(x).widget()
            if widget is not None: 
                widget.deleteLater()
            else:
                if layout.takeAt(x) is not None:
                    self.clear_layout(layout.takeAt(x).layout())

    def clear_all(self):
        children = []
        for i in range(self.main_layout.count()):
            child = self.main_layout.itemAt(i).widget()
            if child:
                children.append(child)
            child = self.main_layout.itemAt(i).layout()
            if child:
                children.append(child)
        for child in children:
            child.deleteLater()
