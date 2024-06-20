import os
import time

import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QLabel, QWidget, QMenuBar, QMenu, QStatusBar, QAction, QFileDialog, QApplication, \
    QMainWindow, QMessageBox

from CircleDialog import CircleDialog
from GaussianDialog import GaussianDialog
from InfoWindow import InfoWindow

BASE_IMAGES_DIR = './Images/'
BASE_IMAGE_NAME = 'cam.png'
BASE_CHANGE_IMAGE_NAME = 'result.png'
BASE_NEGATIVE_IMAGE_NAME = 'negative.png'
BASE_GAUSSIAN_BLUR_IMAGE_NAME = 'gaussian.png'
BASE_RED_CIRCLE_IMAGE_NAME = 'red_circle.png'


class UiMainWindow(object):
    def __init__(self, main_window: QMainWindow):
        self.actionRedCircle = None
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

        self.actionRedCircle = QAction(self.MainWindow)
        self.actionRedCircle.setObjectName("redCircle")
        self.actionRedCircle.triggered.connect(lambda: self.add_red_circle())

        self.actionGet_info_about = QAction(self.MainWindow)
        self.actionGet_info_about.setObjectName("actionGet_info_about")
        self.actionGet_info_about.triggered.connect(lambda: self.get_info_about())

        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionWebCam)

        self.menuEdit.addAction(self.color_channel_menubar.menuAction())
        self.menuEdit.addAction(self.actionNegative)
        self.menuEdit.addAction(self.actionGaussianBlur)
        self.menuEdit.addAction(self.actionRedCircle)

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

        self.actionRedCircle.setText(_translate("MainWindow", "Add red circle"))
        self.actionRedCircle.setStatusTip(_translate("MainWindow", "Add the red circle on the image"))
        self.actionRedCircle.setShortcut(_translate("MainWindow", "Alt+3"))

        self.actionGet_info_about.setText(_translate("MainWindow", "Get info about"))

    def get_info_about(self):
        """
        Метод открывает диалоговое окно, в котором содержится информация о программе
        :return:
        """
        dialog = InfoWindow()
        if dialog.exec_():
            print('hu')
        return None

    def open_gaussian_dialog(self):
        """
        Метод открывает диалоговое окно, в котором пользователь вводит параметры для
        размытия по гауссу
        :return:
        """
        dialog = GaussianDialog()
        if dialog.exec_():
            param = dialog.param1.text()
            return param
        return None

    def open_red_circle_dialog(self):
        """
        Метод открывает диалоговое окно, в котором пользователь вводит параметры для
        создания красного круга на изображении
        :return:
        """
        self.check_file()
        dialog = CircleDialog(self.file_name)
        if dialog.exec_():
            param1 = dialog.param1.text()
            param2 = dialog.param2.text()
            param3 = dialog.param3.text()
            return param1, param2, param3
        return None

    def add_red_circle(self):
        """
        Метод добавляет красный круг с заданными параметрами пользователем
        :return:
        """
        params = self.open_red_circle_dialog()

        if not params:
            return

        try:
            params = tuple(map(int, params))
            # params хранит в себе (координаты по X, координаты по Y, радиус)

            image = cv.imread(self.get_relative_path_from_absolute())

            image_with_red_circle = cv.circle(image, center=(params[0], params[1]), radius=params[2], color=(0, 0, 255),
                                              thickness=-1)

            cv.imwrite(f'{BASE_IMAGES_DIR}{BASE_RED_CIRCLE_IMAGE_NAME}', image_with_red_circle)
            self.set_absolute_path_from_relative(f'{BASE_IMAGES_DIR}{BASE_RED_CIRCLE_IMAGE_NAME}')
            self.label.setPixmap(QPixmap(self.file_name[0]))
        except Exception as e:
            self.label_text.clear()
            self.show_error_message("Please, choose the image")
            print(e)

    def gaussian_blur(self):
        """
        Метод использует размытие изображения по гауссу
        :return:
        """
        self.check_file()
        param = self.open_gaussian_dialog()

        if not param:
            return

        try:
            param = int(param)
            image = cv.imread(self.get_relative_path_from_absolute())

            img_blur = cv.GaussianBlur(image, (param, param), 0)

            cv.imwrite(f'{BASE_IMAGES_DIR}{BASE_GAUSSIAN_BLUR_IMAGE_NAME}', img_blur)
            self.set_absolute_path_from_relative(f'{BASE_IMAGES_DIR}{BASE_GAUSSIAN_BLUR_IMAGE_NAME}')
            self.label.setPixmap(QPixmap(self.file_name[0]))
        except Exception as e:
            self.label_text.clear()
            self.show_error_message("Please, choose the image")
            print(e)

    def show_negative(self):
        """
        Метод сохраняет и отображает негативное изображение
        Негативное изображение сохраняется в ./Images/negative.png
        :return:
        """
        self.check_file()

        try:
            image = cv.imread(self.get_relative_path_from_absolute())
            image = cv.bitwise_not(image)
            cv.imwrite(f'{BASE_IMAGES_DIR}{BASE_NEGATIVE_IMAGE_NAME}', image)
            self.set_absolute_path_from_relative(f'{BASE_IMAGES_DIR}{BASE_NEGATIVE_IMAGE_NAME}')
            self.label.setPixmap(QPixmap(self.file_name[0]))
        except Exception as e:
            self.label_text.clear()
            self.show_error_message("Please, choose the image")
            print(e)

    def open_action(self):
        """
        Метод загружает выбранное изображение из проводника
        Разрешение изображений - .jpg, *.png
        """
        self.file_name = ('', '')
        while self.file_name == ('', ''):
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
        self.check_file()

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

            self.set_absolute_path_from_relative(f'{BASE_IMAGES_DIR}{BASE_CHANGE_IMAGE_NAME}')
            self.label.setPixmap(QPixmap(self.file_name[0]))
            self.label_text.clear()

        except Exception as e:
            self.label_text.clear()
            self.show_error_message("Please, choose the image")
            print(e)

    def check_file(self):
        """
        Метод проверяет на то, чтобы self.file_name не был None или без пути
        :return:
        """
        if self.file_name is None or self.file_name == ('', ''):
            self.show_error_message("Please, choose the image")
            QApplication.processEvents()
            self.open_action()

            self.label_text.clear()
            QApplication.processEvents()

    def get_relative_path_from_absolute(self):
        """
        Преобразует из абсолютного пути в относительный путь.
        Путь - выбранное пользователем изображение
        :return relative_path:
        """
        relative_path = os.path.relpath(self.file_name[0], os.getcwd())
        return relative_path

    def set_absolute_path_from_relative(self, path: str):
        """
        Данный метод сохраняет в self.file_name[0] новый путь с изменённым изображением.
        Меняется выбранное изображение
        :param path:
        :return None:
        """
        absolute_path = os.path.abspath(path)
        self.file_name = (absolute_path, self.file_name[1])

    def show_error_message(self, message: str):
        """
        На экран выводится сообщение об ошибке, с просьбой к пользователю, которая хранится в
        message: str.
        :param message:
        :return:
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(message)
        msg.setWindowTitle("Error")
        msg.exec_()
