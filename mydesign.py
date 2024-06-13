import os
import time

import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QLabel, QWidget, QMenuBar, QMenu, QStatusBar, QAction, QFileDialog, QApplication, \
    QMainWindow
from Dialog import Dialog

BASE_IMAGES_DIR = './Images/'
BASE_IMAGE_NAME = 'cam.png'
BASE_CHANGE_IMAGE_NAME = 'result.png'
BASE_NEGATIVE_IMAGE_NAME = 'negative.png'


class UiMainWindow(object):
    def __init__(self, main_window: QMainWindow):
        self.color_channel_menubar = None
        self.actionGaussianBlur = None
        self.actionNegative = None
        self.label_text = None
        self.actionShowGreenChannel = None
        self.actionShowBlueChannel = None
        self.actionShowRedChannel = None
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
        """
        Содержит всю информацию об окне.
        Настраивается вся информация о геометрии, о меню.
        Настраивается логика кнопок
        :return:
        """
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

        self.color_channel_menubar = QMenu(self.menuEdit)
        self.color_channel_menubar.setObjectName("color_channel_menubar")

        self.actionShowRedChannel = QAction(self.MainWindow)
        self.actionShowRedChannel.setObjectName("showRedChannel")
        self.actionShowRedChannel.triggered.connect(lambda: self.show_channel('RED'))

        self.actionShowGreenChannel = QAction(self.MainWindow)
        self.actionShowGreenChannel.setObjectName("showGreenChannel")
        self.actionShowGreenChannel.triggered.connect(lambda: self.show_channel('GREEN'))

        self.actionShowBlueChannel = QAction(self.MainWindow)
        self.actionShowBlueChannel.setObjectName("showBlueChannel")
        self.actionShowBlueChannel.triggered.connect(lambda: self.show_channel('BLUE'))

        self.color_channel_menubar.addAction(self.actionShowRedChannel)
        self.color_channel_menubar.addAction(self.actionShowGreenChannel)
        self.color_channel_menubar.addAction(self.actionShowBlueChannel)

        self.actionNegative = QAction(self.MainWindow)
        self.actionNegative.setObjectName("negative")
        self.actionNegative.triggered.connect(lambda: self.show_negative())

        self.actionGaussianBlur = QAction(self.MainWindow)
        self.actionGaussianBlur.setObjectName("gaussianBlur")
        self.actionGaussianBlur.triggered.connect(lambda: self.gaussian_blur())

        self.actionGet_info_about = QAction(self.MainWindow)
        self.actionGet_info_about.setObjectName("actionGet_info_about")

        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionWebCam)

        self.menuEdit.addAction(self.color_channel_menubar.menuAction())
        self.menuEdit.addAction(self.actionNegative)
        self.menuEdit.addAction(self.actionGaussianBlur)

        self.menuInfo.addAction(self.actionGet_info_about)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuInfo.menuAction())

        # Создание поля с отображением фотографии
        self.label_text = QLabel(self.central_widget)
        self.label_text.setFont(QFont('Arial', 40))
        self.label_text.setGeometry(QtCore.QRect(280, 20, 681, 60))
        self.label_text.setAlignment(Qt.AlignCenter)
        self.label_text.setStyleSheet("color: #ffffff;")

        self.label = QLabel(self.central_widget)
        self.label.setGeometry(QtCore.QRect(160, 110, 971, 531))

        # pixmap = QPixmap('cat.jpg')
        # self.label.setPixmap(pixmap)

        self.translate_ui()
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

    def translate_ui(self):
        """
        Метод предназначен для локализации пользовательского интерфейса приложения
        :return:
        """
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

        self.color_channel_menubar.setTitle(_translate("MainWindow", "Show color channel"))

        self.actionShowRedChannel.setText(_translate("MainWindow", "Show Red Channel"))
        self.actionShowRedChannel.setStatusTip(_translate("MainWindow", "Show the Red Channel of the image"))
        self.actionShowRedChannel.setShortcut(_translate("MainWindow", "Ctrl+1"))

        self.actionShowGreenChannel.setText(_translate("MainWindow", "Show Green Channel"))
        self.actionShowGreenChannel.setStatusTip(_translate("MainWindow", "Show the Green Channel of the image"))
        self.actionShowGreenChannel.setShortcut(_translate("MainWindow", "Ctrl+2"))

        self.actionShowBlueChannel.setText(_translate("MainWindow", "Show Blue Channel"))
        self.actionShowBlueChannel.setStatusTip(_translate("MainWindow", "Show the Blue Channel of the image"))
        self.actionShowBlueChannel.setShortcut(_translate("MainWindow", "Ctrl+3"))

        self.actionNegative.setText(_translate("MainWindow", "Show negative image"))
        self.actionNegative.setStatusTip(_translate("MainWindow", "Show negative image"))
        self.actionNegative.setShortcut(_translate("MainWindow", "Alt+1"))

        self.actionGaussianBlur.setText(_translate("MainWindow", "Gaussian Blur"))
        self.actionGaussianBlur.setStatusTip(_translate("MainWindow", "Show Gaussian Blur the image"))
        self.actionGaussianBlur.setShortcut(_translate("MainWindow", "Alt+2"))

        self.actionGet_info_about.setText(_translate("MainWindow", "Get info about"))

    def open_dialog(self):
        dialog = Dialog()
        if dialog.exec_():
            param = dialog.param1.text()
        return param

    def gaussian_blur(self):
        param = self.open_dialog()
        print(param)

    def show_negative(self):
        """
        Метод сохраняет и отображает негативное изображение
        Негативное изображение сохраняется в ./Images/negative.png
        :return:
        """
        if self.file_name is None:
            self.label_text.setText("Please, choose the image")
            QApplication.processEvents()
            self.open_action()

        self.label_text.clear()
        QApplication.processEvents()
        try:
            image = cv.imread(self.get_relative_path_from_absolute())
            image = cv.bitwise_not(image)
            cv.imwrite(f'{BASE_IMAGES_DIR}{BASE_NEGATIVE_IMAGE_NAME}', image)
            self.label.setPixmap(QPixmap(f'{BASE_IMAGES_DIR}{BASE_NEGATIVE_IMAGE_NAME}'))

        except Exception as e:
            print(e)

    def open_action(self):
        """
        Метод загружает выбранное изображение из проводника
        Разрешение изображений - .jpg, *.png
        """
        self.file_name = QFileDialog.getOpenFileName(parent=None, caption='Open a file', directory=BASE_IMAGES_DIR,
                                                     filter='Images (*.jpg *.png)')

        self.label.setPixmap(QPixmap(self.file_name[0]))

    def make_photo_by_web_cam(self):
        """
        Метод делает фотоснимок с веб-камеры пользователя.
        Когда сделан снимок, то открывается проводник.
        Пользователю предлагается выбрать изображение самому.
        Снимок с веб-камеры сохраняется в ./Images/cam.png
        :return:
        """
        cap = cv.VideoCapture(0)

        # "Прогреваем" камеру, чтобы снимок не был тёмным
        for i in range(30):
            cap.read()

        self.label_text.setText('PLEASE, READY:')
        self.label.clear()
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

        ret, frame = cap.read()

        cv.imwrite(f'{BASE_IMAGES_DIR}{BASE_IMAGE_NAME}', frame)
        # Отключаем камеру
        cap.release()

        self.label_text.clear()
        self.open_action()

    def show_channel(self, color: str):
        """
        Данный метод создаёт изображение, в котором отображён один из каналов:
        1. Красный (color == 'RED')
        2. Зелёный (color == 'GREEN')
        3. Синий (color == 'BLUE')
        Готовое изображение сохраняется в .Images/result.png
        :param color:
        :return:
        """
        if self.file_name is None:
            self.label_text.setText("Please, choose the image")
            QApplication.processEvents()
            self.open_action()

        self.label_text.clear()
        QApplication.processEvents()
        try:
            self.label_text.setText("Please, wait")
            QApplication.processEvents()
            time.sleep(2)
            self.label.clear()
            QApplication.processEvents()

            image = cv.imread(self.get_relative_path_from_absolute())
            image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

            kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
            image = cv.filter2D(image, -1, kernel)

            hsv_image = cv.cvtColor(image, cv.COLOR_RGB2HSV)

            if color.upper() == 'RED':
                low_color_hsv_1 = (0, 120, 70)
                high_color_hsv_1 = (10, 255, 255)
                low_color_hsv_2 = (170, 120, 70)
                high_color_hsv_2 = (180, 255, 255)

                mask1 = cv.inRange(hsv_image, low_color_hsv_1, high_color_hsv_1)
                mask2 = cv.inRange(hsv_image, low_color_hsv_2, high_color_hsv_2)

                mask = mask1 + mask2

            elif color.upper() == 'GREEN':
                low_color_hsv = (35, 100, 50)
                high_color_hsv = (85, 255, 255)

                mask = cv.inRange(hsv_image, low_color_hsv, high_color_hsv)
            elif color.upper() == 'BLUE':
                low_color_hsv = (100, 150, 0)
                high_color_hsv = (140, 255, 255)

                mask = cv.inRange(hsv_image, low_color_hsv, high_color_hsv)
            else:
                self.label_text.setText("Please, choose the image")
                self.open_action()
                return
            low_white = (0, 0, 200)
            high_white = (145, 60, 255)
            mask_white = cv.inRange(hsv_image, low_white, high_white)

            final_mask = mask + mask_white

            result = cv.imread(f'{BASE_IMAGES_DIR}{BASE_IMAGE_NAME}')
            result = cv.bitwise_and(image, image, result, final_mask)

            contours, hierarchy = cv.findContours(mask.copy(), cv.RETR_TREE,
                                                  cv.CHAIN_APPROX_SIMPLE)
            result = cv.drawContours(result, contours, -1, (161, 255, 255), 3, cv.LINE_AA,
                                     hierarchy, 1)

            plt.imsave(f'{BASE_IMAGES_DIR}{BASE_CHANGE_IMAGE_NAME}', result)

            self.label.setPixmap(QPixmap(f'{BASE_IMAGES_DIR}{BASE_CHANGE_IMAGE_NAME}'))
            self.label_text.clear()

        except Exception as e:
            print(e)

    def get_relative_path_from_absolute(self):
        """
        Преобразует из абсолютного пути в относительный путь.
        Путь - выбранное пользователем изображение
        :return relative_path:
        """
        relative_path = os.path.relpath(self.file_name[0], os.getcwd())
        return relative_path
