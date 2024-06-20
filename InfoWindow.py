from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QPushButton, QDialog, QFormLayout, QLabel


class InfoWindow(QDialog):
    """
    В данном классе создаётся диалоговое окно с информацией о программе
    """
    def __init__(self):
        """
        В методе инициализируется класс и обрабатываются все необходимые поля.
        """
        super().__init__()
        self.setWindowTitle("Info")

        self.layout = QFormLayout()

        info_label = QLabel("Info About program.\n"
                            "If you want to:\n"
                            "open a new image, use: File - Open or 'Ctrl + N';\n"
                            "load photo from WebCam, use: File - Load from WebCam or 'Ctrl + W';\n"
                            "show the red channel of the image, use: Edit - Show color channel - Show "
                            "Red Channel or 'Ctrl + 1';\n"
                            "show the green channel of the image, use: Edit - Show color channel - Show "
                            "Green Channel or 'Ctrl + 2';\n"
                            "show the blue channel of the image, use: Edit - Show color channel - Show "
                            "Blue Channel or 'Ctrl + 3';\n"
                            "show negative image, use: Edit - Show negative image;\n"
                            "show gaussian blur, use: Edit - Gaussian Blur;\n"
                            "add red circle, use: Edit - Add red circle."
                            )
        font = QFont("Arial", 13)
        info_label.setFont(font)
        self.layout.addWidget(info_label)

        self.ok_button = QPushButton("Ok")
        self.ok_button.clicked.connect(self.accept)

        self.layout.addRow(self.ok_button)

        self.setLayout(self.layout)
