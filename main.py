import sys
from PyQt5 import QtWidgets
from MainWindow import MainWindow


def main():
    app = QtWidgets.QApplication(sys.argv)
    b = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
