import time

import cv2 as cv
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QLabel, QWidget, QMenuBar, QMenu, QStatusBar, QAction, QFileDialog, QApplication
BASE_IMAGES_DIR = './Images/'
BASE_NAME = 'cam.png'


class UiMainWindow(object):
    def __init__(self, main_window):
        self.file_name = None
        self.MainWindow = main_window
        self.label = None
        self.actionGet_info_about = None
        self.actionSave = None
        self.actionOpen = None
        self.statusbar = None
        self.menuInfo = None
        self.menuEdit = None
        self.menuFile = None
        self.menubar = None
        self.central_widget = None
        self.actionWebCam = None

    def setup_ui(self):
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(1280, 720)

        # Установка центрального виджета
        self.central_widget = QWidget(self.MainWindow)
        self.central_widget.setObjectName("centralwidget")
        self.MainWindow.setCentralWidget(self.central_widget)
        self.central_widget.setStyleSheet("background-color: #333;")

        # Установка MenuBar
        self.menubar = QMenuBar(self.MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 21))
        self.menubar.setInputMethodHints(QtCore.Qt.ImhNone)
        self.menubar.setObjectName("menubar")
        self.menubar.setStyleSheet("""
        QMenuBar {
            background-color: #3d3d3d; 
            color: #ffffff;
        }
        QMenuBar::item {
            background-color: #3d3d3d; 
            color: #ffffff;
        }
        QMenuBar::item:selected {
            background-color: #999999;
            color: #ffffff;
        }
        QMenuBar::item:pressed {
            background-color: #525252;
            color: #ffffff;
        }
        QMenu::item {
            background-color: #3d3d3d; 
            color: #ffffff;
        }
        QMenu::item:selected {
            background-color: #999999;
            color: #ffffff;
        }
        QMenu::item:pressed {
            background-color: #525252;
            color: #ffffff;
        }
        """)
        # self.menubar.setStyleSheet("QMenuBar::item:selected { background-color: #3d3d3d; color: #ffffff; }")
        # self.menubar.setStyleSheet("QMenuBar::item:pressed { background-color: #aaaaaa; color: #ffffff; }")

        # Установка пункта File
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")

        # Установка пункта Edit
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")

        # Установка пункта Info
        self.menuInfo = QMenu(self.menubar)
        self.menuInfo.setObjectName("menuInfo")

        # Установка menubar 
        self.MainWindow.setMenuBar(self.menubar)

        # Создание statusBar
        self.statusbar = QStatusBar(self.MainWindow)
        self.statusbar.setEnabled(True)
        self.statusbar.setObjectName("statusbar")
        self.statusbar.setStyleSheet(" background-color: #3d3d3d; color: #ffffff;")
        self.MainWindow.setStatusBar(self.statusbar)

        # Обработка нажатий на кнопки File, Edit, Info
        self.actionOpen = QAction(self.MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionOpen.triggered.connect(lambda: self.open_action())

        self.actionSave = QAction(self.MainWindow)
        self.actionSave.setObjectName("actionSave")

        self.actionWebCam = QAction(self.MainWindow)
        self.actionWebCam.setObjectName("actionLoad_from_WebCam")
        self.actionWebCam.triggered.connect(lambda: self.make_photo_by_web_cam())

        self.actionGet_info_about = QAction(self.MainWindow)
        self.actionGet_info_about.setObjectName("actionGet_info_about")

        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionWebCam)
        self.menuInfo.addAction(self.actionGet_info_about)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuInfo.menuAction())

        # Создание поля с отображением фотографии
        self.label = QLabel(self.central_widget)
        self.label.setGeometry(QtCore.QRect(160, 30, 911, 591))

        self.label_text = QLabel(self.central_widget)
        self.label_text.setFont(QFont('Arial', 40))
        self.label_text.setGeometry(QtCore.QRect(280, 20, 681, 60))
        self.label_text.setAlignment(Qt.AlignCenter)
        self.label_text.setStyleSheet("color: #ffffff;")
        # pixmap = QPixmap('cat.jpg')
        # self.label.setPixmap(pixmap)

        self.translate_ui()
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

    def translate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.MainWindow.setWindowTitle(_translate("MainWindow", "summerPractice"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuInfo.setTitle(_translate("MainWindow", "Info"))

        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen.setStatusTip(_translate("MainWindow", "Open a file"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+N"))

        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setStatusTip(_translate("MainWindow", "Save a file"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))

        self.actionWebCam.setText(_translate("MainWindow", "Load from WebCam"))
        self.actionWebCam.setStatusTip(_translate("MainWindow", "Load from WebCam"))
        self.actionWebCam.setShortcut(_translate("MainWindow", "Ctrl+W"))

        self.actionGet_info_about.setText(_translate("MainWindow", "Get info about"))

    def open_action(self):
        """
        Метод загружает выбранное изображение из проводника
        Разрешение изображений - .jpg, *.png
        """
        self.file_name = QFileDialog.getOpenFileName(parent=None, caption='Open a file', directory=BASE_IMAGES_DIR,
                                                     filter='Images (*.jpg *.png)')

        self.label.setPixmap(QPixmap(self.file_name[0]))

    def make_photo_by_web_cam(self):
        cap = cv.VideoCapture(0)

        # "Прогреваем" камеру, чтобы снимок не был тёмным
        for i in range(30):
            cap.read()

        self.label_text.setText('PLEASE, READY:')
        QApplication.processEvents()
        time.sleep(1)

        self.label_text.setText('1')
        QApplication.processEvents()
        time.sleep(1)

        self.label_text.setText('2')
        QApplication.processEvents()
        time.sleep(1)

        self.label_text.setText('3')
        QApplication.processEvents()

        start_time = time.time()

        ret, frame = cap.read()

        cv.imwrite(f'{BASE_IMAGES_DIR}{BASE_NAME}', frame)
        # Отключаем камеру
        cap.release()
        end_time = time.time()
        print(end_time - start_time)
        self.label_text.clear()
        self.open_action()
