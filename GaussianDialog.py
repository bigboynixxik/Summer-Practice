from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QPushButton, QLineEdit, QDialog, QFormLayout, QLabel, QMessageBox


class GaussianDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Input data")

        self.layout = QFormLayout()

        info_label = QLabel("Enter an odd integer for the kernel size.")
        self.layout.addWidget(info_label)

        self.param1 = QLineEdit()
        odd_number_validator = QIntValidator()
        odd_number_validator.setRange(1, 1000000)  # установите допустимый диапазон по нечетным числам
        self.param1.setValidator(odd_number_validator)

        self.layout.addRow("Kernel size", self.param1)

        self.ok_button = QPushButton("Ok")
        self.ok_button.clicked.connect(self.check_input)

        self.layout.addRow(self.ok_button)

        self.setLayout(self.layout)

    def check_input(self):
        input_text = self.param1.text()
        if not input_text.isdigit():
            self.show_error_message("Please enter a valid integer.")
            return

        kernel_size = int(input_text)
        if kernel_size % 2 == 0:
            self.show_error_message("Please enter an odd integer.")
            return

        # если все хорошо, закрыть диалоговое окно
        self.accept()

    def show_error_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(message)
        msg.setWindowTitle("Error")
        msg.exec_()
