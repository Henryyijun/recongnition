import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QLockFile, QDir
from MainWindow import MainWindow


def main():
    app = QtWidgets.QApplication(sys.argv)
    b = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    file = QLockFile(f'{QDir.tempPath()}/single_app.lock')
    file.setStaleLockTime(0)
    if not file.tryLock():  # 防止多开
        sys.exit(0)
    main()
