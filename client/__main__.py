from ctypes import ArgumentError
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QComboBox, QCheckBox, QPushButton, QTextEdit, QGridLayout, QMessageBox
from PySide6.QtGui import QIntValidator, QDoubleValidator
from numpy import who
import requests


class HealthApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Health App")
        self.resize(600, 400)
        self.initUI()

    def initUI(self):
        self.age_label = QLabel("Возраст:")
        self.age_edit = QLineEdit()
        self.age_edit.setValidator(QIntValidator(18, 100))

        self.gender_label = QLabel("Пол:")
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Мужской", "Женский"])

        self.sbp_label = QLabel("Верхнее давление:")
        self.sbp_edit = QLineEdit()
        self.sbp_edit.setValidator(QIntValidator(70, 300))

        self.dbp_label = QLabel("Нижнее давление:")
        self.dbp_edit = QLineEdit()
        self.sbp_edit.setValidator(QIntValidator(40, 200))

        self.cholesterol_label = QLabel("Уровень холестерина:")
        self.cholesterol_combo = QComboBox()
        self.cholesterol_combo.addItems(["1", "2", "3"])

        self.glucose_label = QLabel("Уровень глюкозы:")
        self.glucose_combo = QComboBox()
        self.glucose_combo.addItems(["1", "2", "3"])

        self.alcohol_label = QLabel("Употребление алкоголя:")
        self.alcohol_check = QCheckBox("Да")

        self.smoking_label = QLabel("Курение:")
        self.smoking_check = QCheckBox("Да")

        self.active_label = QLabel("Активный образ жизни:")
        self.active_check = QCheckBox("Да")

        self.bmi_label = QLabel("BMI:")
        self.bmi_edit = QLineEdit()
        self.bmi_edit.setValidator(QDoubleValidator(10, 50, 2))

        widgets = [
                (self.age_label, self.age_edit),
                (self.gender_label, self.gender_combo),
                (self.sbp_label, self.sbp_edit),
                (self.dbp_label, self.dbp_edit),
                (self.cholesterol_label, self.cholesterol_combo),
                (self.glucose_label, self.glucose_combo),
                (self.alcohol_label, self.alcohol_check),
                (self.smoking_label, self.smoking_check),
                (self.active_label, self.active_check),
                (self.bmi_label, self.bmi_edit),
        ]

        self.submit_button = QPushButton("Отправить")
        self.submit_button.clicked.connect(self.submit)

        self.answer_text = QTextEdit()
        self.answer_text.setReadOnly(True)

        self.grid = QGridLayout()
        for i, widget in enumerate(widgets):
            self.grid.addWidget(widget[0], i, 0)
            self.grid.addWidget(widget[1], i, 1)
        self.grid.addWidget(self.submit_button, len(widgets), 0, 1, 2)
        self.grid.addWidget(self.answer_text, len(widgets) + 1, 0, 1, 2)

        self.setLayout(self.grid)

    def submit(self):
        try:
            data = self.fetch_data()
        except ArgumentError:
            QMessageBox.warning(self, "Предупреждение", "Пожалуйста, заполните все поля.")
            return
        ans = requests.post("http://31.31.202.46:6969", json=data).json()["prediction"]
        if ans:
            self.answer_text.setText("У пациента присутствуют сердечно-сосудистые заболевания.")
        else:
            self.answer_text.setText("У пациента отсутствуют сердечно-сосудистые заболевания.")


    def fetch_data(self):
        if not (self.sbp_edit.text() and self.dbp_edit.text() and self.bmi_edit.text()):
            raise ArgumentError
        return {
                "age": int(self.age_edit.text()),
                "gender": 1 if self.gender_combo.currentText() == "Мужской" else 0,
                "ap_hi": int(self.sbp_edit.text()),
                "ap_lo": int(self.dbp_edit.text()),
                "cholesterol": int(self.cholesterol_combo.currentText()),
                "gluc": int(self.glucose_combo.currentText()),
                "smoke": int(self.smoking_check.isChecked()),
                "alco": int(self.alcohol_check.isChecked()),
                "active": int(self.active_check.isChecked()),
                "bmi": float(self.bmi_edit.text()),
        }


if __name__ == "__main__":
    app = QApplication()
    window = HealthApp()
    window.show()
    app.exec()

