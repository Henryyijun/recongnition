from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtWidgets import QMainWindow

from Ui_loginwindow import Ui_loginWindow


class LoginWindow(QMainWindow):
    IP_signal = pyqtSignal(str, int)

    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_loginWindow()
        self.ui.setupUi(self)
        self.msg_box = QMessageBox(QMessageBox.Warning, "错误", "请输入服务器IP或者端口号")

    @pyqtSlot()
    def on_loginBt_clicked(self):
        print('login')
        IP = self.ui.lineEdit.text()
        PORT = self.ui.lineEdit_2.text()
        if IP == '' or PORT == '':
            self.msg_box.show()
        else:
            PORT = int(PORT)
            self.IP_signal.emit(IP, PORT)
            print("login windows ", IP, PORT)





