from PyQt5.QtGui import QIntValidator, QPixmap
from PyQt5.QtWidgets import QPushButton, QLineEdit, QDialog, QFormLayout, QLabel, QMessageBox


class CircleDialog(QDialog):
    """
    В данном классе создаётся диалоговое окно.
    Обрабатывается информация для создания красного круга на изображении
    """

    def __init__(self, img: tuple):
        """
        В методе инициализируется класс и обрабатываются все необходимые поля.
        От пользователя получаем 3 параметра:
        Координаты центра по X, Y, радиус круга.
        :param img:
        """
        super().__init__()
        self.setWindowTitle("Input data for circle")
        pixmap = QPixmap(img[0])
        image_size = pixmap.size()
        self.layout = QFormLayout()

        info_label = QLabel("Enter an some integer data")
        self.layout.addWidget(info_label)

        self.param1 = QLineEdit()
        number_validator_1 = QIntValidator()
        number_validator_1.setRange(1, image_size.width())
        self.param1.setValidator(number_validator_1)

        self.layout.addRow("X coords of center", self.param1)

        self.param2 = QLineEdit()
        number_validator_2 = QIntValidator()
        number_validator_2.setRange(1, image_size.height())
        self.param2.setValidator(number_validator_2)

        self.layout.addRow("Y coords of center", self.param2)

        self.param3 = QLineEdit()
        number_validator_3 = QIntValidator()
        number_validator_3.setRange(1, image_size.height() // 2)
        self.param3.setValidator(number_validator_3)

        self.layout.addRow("Enter the radius of circle", self.param3)

        self.ok_button = QPushButton("Ok")
        self.ok_button.clicked.connect(self.check_input)

        self.layout.addRow(self.ok_button)

        self.setLayout(self.layout)

    def check_input(self):
        """
        Проверяются все введённые пользователем данные.
        Они должны быть числами
        :return:
        """
        input_text_1 = self.param1.text()
        input_text_2 = self.param2.text()
        input_text_3 = self.param3.text()

        if not input_text_1.isdigit() or not input_text_2.isdigit() or not input_text_3.isdigit():
            self.show_error_message("Please enter a valid integer.")
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
