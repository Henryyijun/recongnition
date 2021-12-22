
import sys
from PyQt5 import QtWidgets
from LoginWindow import LoginWindow
from MainWindow import MainWindow


def main():
    app = QtWidgets.QApplication(sys.argv)
    a = LoginWindow()
    b = MainWindow()
    a.show()
    a.ui.loginBt.clicked.connect(b.show)
    a.ui.loginBt.clicked.connect(a.close)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
