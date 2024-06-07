# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mydesign.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QWidget, QMenuBar, QMenu, QStatusBar, QAction, QFileDialog


class UiMainWindow(object):
    def __init__(self, main_window):
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

    def setup_ui(self):
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(1280, 720)

        # Установка центрального виджета
        self.central_widget = QWidget(self.MainWindow)
        self.central_widget.setObjectName("centralwidget")
        self.MainWindow.setCentralWidget(self.central_widget)

        # Установка MenuBar
        self.menubar = QMenuBar(self.MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 21))
        self.menubar.setInputMethodHints(QtCore.Qt.ImhNone)
        self.menubar.setObjectName("menubar")

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
        self.MainWindow.setStatusBar(self.statusbar)

        # Обработка нажатий на кнопки File, Edit, Info
        self.actionOpen = QAction(self.MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionOpen.triggered.connect(lambda: self.open_action())

        self.actionSave = QAction(self.MainWindow)
        self.actionSave.setObjectName("actionSave")

        self.actionGet_info_about = QAction(self.MainWindow)
        self.actionGet_info_about.setObjectName("actionGet_info_about")

        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuInfo.addAction(self.actionGet_info_about)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuInfo.menuAction())

        # Создание поля с отображением фотографии
        self.label = QLabel(self.central_widget)
        self.label.setGeometry(QtCore.QRect(160, 30, 911, 591))
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
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setStatusTip(_translate("MainWindow", "Save a file"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionGet_info_about.setText(_translate("MainWindow", "Get info about"))

    def open_action(self):
        """
        Метод загружает выбранное изображение из проводника
        Разрешение изображений - .jpg, *.png
        """
        file_name = QFileDialog.getOpenFileName(parent=None, caption='Open a file', directory='./',
                                                filter='Images (*.jpg *.png)')
        self.label.setPixmap(QPixmap(file_name[0]))