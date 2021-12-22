from PyQt5.QtCore import pyqtSlot, QFileInfo, pyqtSignal, QBuffer, QByteArray, QIODevice, QSize, Qt
from PyQt5.QtWidgets import QWidget, QFileDialog, QLabel
from PyQt5.QtWidgets import QMainWindow
from Ui_loginwindow import Ui_loginWindow


class LoginWindow(QMainWindow):
    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_loginWindow()
        self.ui.setupUi(self)

    @pyqtSlot()
    def on_loginBt_clicked(self):
        print('login')




