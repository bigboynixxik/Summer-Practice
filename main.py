from PyQt5 import QtWidgets

from mydesign import UiMainWindow

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UiMainWindow(MainWindow)
    ui.setup_ui()
    MainWindow.show()
    sys.exit(app.exec_())
