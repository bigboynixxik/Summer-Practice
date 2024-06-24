from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QPushButton, QLineEdit, QDialog, QFormLayout, QLabel, QMessageBox


class GaussianDialog(QDialog):
    """
    В данном классе создаётся диалоговое окно.
    Обрабатывается информация для создания размытия по Гауссу
    """

    def __init__(self):
        """
        В методе инициализируется класс и обрабатываются все необходимые поля.
        Принимается один параметр - размер ядра
        """
        super().__init__()
        self.setWindowTitle("Input data")

        self.layout = QFormLayout()

        info_label = QLabel("Enter an odd integer for the kernel size.")
        self.layout.addWidget(info_label)

        self.param1 = QLineEdit()
        odd_number_validator = QIntValidator()
        odd_number_validator.setRange(1, 501)
        self.param1.setValidator(odd_number_validator)

        self.layout.addRow("Kernel size", self.param1)

        self.ok_button = QPushButton("Ok")
        self.ok_button.clicked.connect(self.check_input)

        self.layout.addRow(self.ok_button)

        self.setLayout(self.layout)

    def check_input(self):
        """
        Проверяются введённые данные.
        Размер ядра должен быть нечётным числом
        :return:
        """
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

    def show_error_message(self, message: str):
        """
        В случае ошибки, выводится сообщение о ней
        :param message:
        :return:
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(message)
        msg.setWindowTitle("Error")
        msg.exec_()
